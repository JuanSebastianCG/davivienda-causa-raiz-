import re

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import seaborn as sns
from src.configs.config import logger


def plot_joint_distribution(
    df,
    x,
    y,
    x_order=None,
    y_order=None,
    label_rotation=0,
    palette="rebeccapurple",
    x_label=None,
    y_label=None,
    top_x=None,
    top_y=None,
    fontsize=10,
    title="",
    path_save="",
):
    sns.set_theme(style="ticks")

    # Obtener los valores con mayor frecuencia en x
    if top_x is not None:
        top_x_values = df[x].value_counts().nlargest(top_x).index
        df = df[df[x].isin(top_x_values)]

    # Obtener los valores con mayor frecuencia en y
    if top_y is not None:
        top_y_values = df[y].value_counts().nlargest(top_y).index
        df = df[df[y].isin(top_y_values)]

    # Convertir las columnas a categóricas si tienen un orden especificado
    if x_order is not None:
        df[x] = pd.Categorical(df[x], categories=x_order, ordered=True)
    if y_order is not None:
        df[y] = pd.Categorical(df[y], categories=y_order, ordered=True)

    # Crear el gráfico conjunto
    g = sns.JointGrid(
        data=df,
        x=x,
        y=y,
        marginal_ticks=True,
        palette=palette,
    )

    # Añadir los gráficos de histograma conjunto y marginal
    g.plot_joint(
        sns.histplot,
        cmap="light:#773dbd",
        pmax=0.8,
    )
    g.plot_marginals(sns.histplot, element="step", color=palette)

    # Rotar etiquetas de los ticks del eje x
    for label in g.ax_joint.get_xticklabels():
        label.set_rotation(label_rotation)
        label.set_ha("right")

    # Añadir etiquetas de porcentaje dentro del gráfico conjunto
    hist_data = df.groupby([x, y]).size().reset_index(name="counts")
    total_counts = hist_data["counts"].sum()
    hist_data["percentage"] = (hist_data["counts"] / total_counts) * 100
    for row in hist_data.itertuples():
        if row.percentage > 0:
            g.ax_joint.text(
                row[1],
                row[2],
                f"{row.percentage:.1f}%",
                ha="center",
                va="center",
                size=fontsize,
            )

    # Establecer etiquetas de los ejes x e y
    g.set_axis_labels(x_label if x_label else x, y_label if y_label else y)

    if title == "Peticiones":
        left_title = -0.33
    elif title == "Quejas":
        left_title = -0.37
    elif title == "Reclamos":
        left_title = -0.2
    else:
        left_title = -0.3

    # Añadir título
    g.figure.suptitle(title, fontsize=fontsize + 4, color="black", fontweight="bold", x=left_title)

    return g.figure


def plot_bar_percentage(
    df,
    col,
    percentage: float = 100,
    start_color: str = "#773dbd",
    end_color: str = "#b58fe6",
    title: str = "",
):
    if df.empty:
        raise ValueError(
            "The DataFrame is empty. Please provide a DataFrame with data."
        )

    # Calculate cumulative percentage
    total_count = df[col].value_counts().sum()
    if total_count == 0:
        raise ValueError(
            "Total count of the specified column is zero, which will result in division by zero."
        )

    value_counts = df[col].value_counts()
    cumulative_percentage = value_counts.cumsum() / total_count * 100

    # Filter categories that exceed the specified percentage
    filtered_categories = cumulative_percentage[
        cumulative_percentage <= percentage
    ].index

    if len(filtered_categories) == 0:
        raise ValueError(
            "No categories are included within the specified percentage threshold."
        )

    filtered_df = df[df[col].isin(filtered_categories)]

    if filtered_df.empty:
        raise ValueError(
            "Filtered DataFrame is empty after applying the percentage threshold. Adjust the threshold."
        )

    # Create a categorical color map
    unique_categories = filtered_df[col].unique()
    colors = px.colors.sample_colorscale(
        px.colors.make_colorscale([start_color, end_color]),
        [
            i / (len(unique_categories) - 1)
            for i in range(len(unique_categories))
            if len(unique_categories) > 1
        ],
    )
    color_map = {category: colors[i] for i, category in enumerate(unique_categories)}

    # Create the bar chart
    fig = px.histogram(
        filtered_df,
        y=col,
        color=col,
        color_discrete_map=color_map,
        category_orders={col: value_counts.loc[filtered_categories].index.tolist()},
        width=800,
        height=400,
    )

    # Hide legend
    fig.update_layout(showlegend=False)

    # Add title and labels
    fig.update_layout(
        title=title,
        xaxis_title="Cantidad",
        yaxis_title=col.capitalize().replace("_", " "),
        template="simple_white",
    )

    # Add percentage annotations
    total = len(filtered_df)
    annotations = []
    for category in filtered_categories:
        count = value_counts[category]
        percentage_text = (
            f"{100 * count / total:.2f}%" if total > 0 else "0%"
        )  # Safeguard against zero division
        annotations.append(
            dict(
                x=count,
                y=category,
                text=percentage_text,
                showarrow=False,
                xanchor="left",
                yanchor="middle",
                font=dict(size=12, color=start_color),
            )
        )

    fig.update_layout(annotations=annotations)

    return fig


def plot_weekly_distribution(df, date_col, color="#773dbd"):
    # Asegurarse de que la columna de fechas esté en formato datetime
    df[date_col] = pd.to_datetime(df[date_col])

    # Extraer el día del mes y la semana del año
    df["day"] = df[date_col].dt.day
    df["week"] = df[date_col].dt.isocalendar().week

    # Contar el número de solicitudes por día
    daily_counts = df.groupby("day").size()

    # Crear el gráfico de barras
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=daily_counts.index,
            y=daily_counts.values,
            marker_color=color,
            width=0.6,
            name="Solicitudes",
        )
    )

    # Añadir divisores y etiquetas para las semanas
    week_starts = df.groupby("week")["day"].min().sort_values()
    for idx, day in enumerate(week_starts):
        fig.add_shape(
            type="line",
            x0=day - 1.5,
            y0=0,
            x1=day - 1.5,
            y1=daily_counts.max(),
            line=dict(color="grey", dash="dash", width=1),
        )
        if idx < len(week_starts) - 1:
            fig.add_annotation(
                x=day + 4,
                y=daily_counts.max() - 5,
                text=f"Semana {idx + 1}",
                showarrow=False,
                font=dict(color="gray"),
                align="center",
            )

    # Configurar las etiquetas y el título
    fig.update_layout(
        title="Distribución de solicitudes por día de apertura",
        xaxis_title="Día del mes",
        yaxis_title="Cantidad de solicitudes",
        title_font_size=14,
        title_font_color="rebeccapurple",
        xaxis=dict(tickmode="linear"),
        yaxis=dict(tickmode="linear"),
    )

    return fig


def plot_weekday_distribution(
    df,
    date_column,
    category_column,
    start_color="#773dbd",
    end_color="#eae0f5",
    n_colors=7,
    order=None,
):
    # Añadir columna del día de la semana
    df["day_of_week"] = df[date_column].dt.dayofweek
    df["day_of_week"] = df["day_of_week"].map(
        {
            0: "Lunes",
            1: "Martes",
            2: "Miércoles",
            3: "Jueves",
            4: "Viernes",
            5: "Sábado",
            6: "Domingo",
        }
    )

    # Agrupar por causa raíz y día de la semana
    df_grouped = df.groupby([category_column, "day_of_week"]).size().unstack().fillna(0)
    df_grouped = (df_grouped.div(df_grouped.sum(axis=1), axis=0) * 100).round(2)

    # Asegurarse de que las columnas estén en el orden correcto
    df_grouped = df_grouped[
        ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    ]

    if order:
        df_grouped = df_grouped.reindex(order)

    # Crear una paleta de colores basada en un degradado
    cmap = px.colors.sample_colorscale(
        px.colors.make_colorscale([start_color, end_color]),
        [n / (n_colors - 1) for n in range(n_colors)],
    )

    # Crear el gráfico de barras apiladas
    fig = go.Figure()

    for idx, day in enumerate(df_grouped.columns):
        fig.add_trace(
            go.Bar(
                x=df_grouped.index, y=df_grouped[day], name=day, marker_color=cmap[idx]
            )
        )

    # Añadir porcentajes a cada barra, omitiendo los 0%
    for i in range(len(fig.data)):
        fig.data[i].text = [f"{val:.1f}%" if val > 3.3 else "" for val in fig.data[i].y]
        fig.data[i].textposition = "inside"

    # Configurar las etiquetas del eje x
    fig.update_xaxes(tickangle=45)

    # Configurar la leyenda
    fig.update_layout(
        barmode="stack",
        legend=dict(title=None, font_size=10, orientation="h", y=1.1, x=0.02),
        title="Distribución porcentual de causas raíz por día de la semana",
        title_font=dict(color="rebeccapurple"),
        xaxis_title="Causa raíz",
        yaxis_title="Porcentaje",
        margin=dict(t=100),
    )

    return fig


def table_percentage(
    df,
    index,
    cols,
    values,
    order=None,
    top=None,
    fontsize=9,
    start_color="#ffffff",
    end_color="#773dbd",
    col_order=None,
):
    if top:
        df_grouped = df.pivot_table(
            index=index, columns=cols, values=values, aggfunc="count"
        ).fillna(0)
        df_grouped = df_grouped.T.head(top)
        print(df_grouped.shape)
    else:
        df_grouped = df.pivot_table(
            index=index, columns=cols, values=values, aggfunc="count"
        ).fillna(0)
    df_grouped = (df_grouped.T / df_grouped.T.sum()) * 100

    if order:
        df_grouped = df_grouped.reindex(order)
    if col_order:
        df_grouped = df_grouped[col_order]

    # Convertir el DataFrame a una lista de listas para plotly.figure_factory.create_annotated_heatmap
    z = df_grouped.values
    x = df_grouped.columns.tolist()
    y = df_grouped.index.tolist()

    # Crear colores para la paleta
    colors = px.colors.sample_colorscale(
        px.colors.make_colorscale([start_color, end_color]),
        [i / 255 for i in range(256)],
    )

    # Crear la tabla de calor anotada
    fig = ff.create_annotated_heatmap(
        z,
        x=x,
        y=y,
        annotation_text=np.round(z, 1),
        colorscale=colors,
        font_colors=["black"],
        hoverinfo="z",
    )

    # Configurar las etiquetas del eje x
    fig.update_xaxes(tickangle=45, side="bottom")

    # Configurar las etiquetas del eje y
    fig.update_yaxes(tickangle=0)

    # Configurar la leyenda y otros aspectos del layout
    fig.update_layout(
        title="Distribución de {} y {}".format(
            index.replace("_", " ").capitalize(), cols.replace("_", " ").capitalize()
        ),
        title_font=dict(size=14, color="rebeccapurple"),
        xaxis_title=cols.replace("_", " ").capitalize(),
        yaxis_title=index.replace("_", " ").capitalize(),
        margin=dict(t=100),
        font=dict(size=fontsize),
    )

    return fig


def plot_pie_chart(
    df,
    col,
    percentage_threshold,
    start_color="#773dbd",
    end_color="#eae0f5",
    n_colors=7,
    legend_title="",
    num_registros=False,
    marker_fontsize=15,
    title_fontsize=20,
    legend_fontsize=14,
    title="",
    legend_y=-0.3,
    legend_x=0.5,
    figsize=(600, 600),
):
    df2 = df.copy()

    # Crear una paleta de colores personalizada
    cmap = px.colors.sample_colorscale(
        px.colors.make_colorscale([start_color, end_color]),
        [i / (n_colors - 1) for i in range(n_colors)],
    )

    # Calcular el porcentaje de cada categoría
    value_counts = df2[col].value_counts()
    total_count = value_counts.sum()
    percentage_counts = value_counts / total_count * 100

    # Reemplazar valores menores al porcentaje especificado por "Otros"
    mask = percentage_counts < percentage_threshold
    df2[col] = df2[col].apply(lambda x: "Otros" if x in mask[mask].index else x)

    # Recalcular los valores después de la agrupación de "Otros"
    value_counts = df2[col].value_counts()
    colors = cmap[
        : len(value_counts)
    ]  # Ajustar la lista de colores al número de categorías

    # Crear el gráfico de pastel
    fig = go.Figure(
        data=[
            go.Pie(
                labels=value_counts.index,
                values=value_counts.values,
                textinfo="percent",
                marker=dict(colors=colors),
                hole=0.6,
            )
        ]
    )

    # Configurar las propiedades del gráfico
    fig.update_traces(
        hoverinfo="label+percent",
        textposition="inside",
        textfont_size=marker_fontsize,
        marker=dict(line=dict(color="#000000", width=0.5)),
    )

    if num_registros:
        text_legend = (
            df2[col].value_counts().index.map(str)
            + " ("
            + df2[col].value_counts().astype(str)
            + " registros)"
        )
    else:
        text_legend = df2[col].value_counts().index.map(str)

    # Ajustar la leyenda
    fig.update_layout(
        legend=dict(
            title=dict(text=legend_title),
            orientation="h",
            yanchor="bottom",
            y=legend_y,
            xanchor="center",
            x=legend_x,
            traceorder="normal",
            font=dict(size=legend_fontsize),
        ),
        title=dict(
            text=title,
            font=dict(size=title_fontsize, color="rebeccapurple"),
            x=0.5,
            xanchor="center",
        ),
        margin=dict(t=100, b=20),
        width=figsize[0],
        height=figsize[1],
    )

    return fig


def plot_stacked_barh(
    df,
    col1,
    col2,
    start_color="#773dbd",
    end_color="#eae0f5",
    n_colors=7,
    xlim=None,
    remove_axes_lines=True,
    rounded_bars=True,
    threshold=5,
):
    # Agrupar los datos y calcular el tamaño de cada grupo
    df_grouped = df.groupby([col1, col2]).size().unstack().fillna(0)

    # Ordenar las barras de la más grande a la más pequeña
    df_grouped = df_grouped.loc[
        :, df_grouped.sum(axis=0).sort_values(ascending=True).index
    ]

    # Ordenar las categorías de la leyenda de mayor a menor
    df_grouped = df_grouped.loc[
        df_grouped.sum(axis=1).sort_values(ascending=False).index
    ]

    # Crear una paleta de colores personalizada basada en el número de categorías
    n_categories = len(df_grouped.columns)
    cmap = px.colors.sample_colorscale(
        px.colors.make_colorscale([start_color, end_color]),
        [i / (n_categories - 1) for i in range(n_categories)],
    )

    # Crear el gráfico de barras horizontales apiladas
    fig = go.Figure()

    for idx, category in enumerate(df_grouped.columns):
        fig.add_trace(
            go.Bar(
                y=df_grouped.index,
                x=df_grouped[category],
                name=category,
                orientation="h",
                marker=dict(color=cmap[idx]),
            )
        )

    # Añadir porcentajes a cada barra respecto al total de la barra
    for trace in fig.data:
        trace.text = [
            f"{100 * v / total:.1f}%" if v / total * 100 >= threshold else ""
            for v, total in zip(trace.x, df_grouped.sum(axis=1))
        ]
        trace.textposition = "inside"

    # Configurar las etiquetas y el título
    fig.update_layout(
        title=dict(
            text=f'Distribución de {col1.capitalize().replace("_"," ")} por {col2.capitalize().replace("_"," ")}',
            font=dict(size=14, color="rebeccapurple"),
            x=0.5,
            xanchor="center",
        ),
        xaxis_title="Cantidad",
        yaxis_title=col2.capitalize().replace("_", " "),
        barmode="stack",
        legend=dict(
            title=dict(text=col1.capitalize()),
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            traceorder="normal",
        ),
        margin=dict(t=100, b=40),
    )

    # Aplicar los límites del eje x si se proporciona
    if xlim is not None:
        fig.update_xaxes(range=xlim)

    # Quitar las líneas de los ejes si se solicita
    if remove_axes_lines:
        fig.update_xaxes(showline=False)
        fig.update_yaxes(showline=False)

    return fig


def plot_linear_weekday_distribution(
    df,
    date_column,
    category_column,
    start_color="#773dbd",
    end_color="#eae0f5",
    n_colors=7,
    order=None,
    threshold=5,  # Umbral para mostrar los valores
):
    # Añadir columna del día de la semana
    df["day_of_week"] = df[date_column].dt.dayofweek
    df["day_of_week"] = df["day_of_week"].map(
        {
            0: "Lunes",
            1: "Martes",
            2: "Miércoles",
            3: "Jueves",
            4: "Viernes",
            5: "Sábado",
            6: "Domingo",
        }
    )

    # Agrupar por causa raíz y día de la semana
    df_grouped = df.groupby([category_column, "day_of_week"]).size().unstack().fillna(0)
    df_grouped = (df_grouped.div(df_grouped.sum(axis=1).sum(), axis=0) * 100).round(2)

    # Asegurarse de que las columnas estén en el orden correcto
    df_grouped = df_grouped[
        ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    ]

    if order:
        df_grouped = df_grouped.reindex(order)

    # Crear una paleta de colores basada en un degradado
    colors = px.colors.sample_colorscale(
        "Viridis", [i / n_colors for i in range(n_colors)]
    )

    # Crear el gráfico de líneas
    fig = go.Figure()

    for idx, (name, values) in enumerate(df_grouped.iterrows()):
        fig.add_trace(
            go.Scatter(
                x=values.index,
                y=values,
                mode="lines+markers+text",
                line=dict(color=colors[idx % len(colors)], width=2),
                text=[f"{val:.2f}%" if val > threshold else "" for val in values],
                textposition="top center",
                name=name,
            )
        )

    # Configurar la leyenda
    fig.update_layout(
        title="Distribución porcentual de causas raíz por día de la semana",
        title_font=dict(color="rebeccapurple"),
        xaxis_title="Día de la semana",
        yaxis_title="Porcentaje [%]",
        template="simple_white",
    )

    return fig


def convert_columns_names(df):
    df.columns = [re.sub(r"\s+", "_", col.lower()) for col in df.columns]
    return df


def process_product_column(
    df, product_col="producto", new_col="producto_", threshold=5
):
    """Procesa la columna del nombre del producto, extrayendo el primer segmento antes del guion y agrupando
    las categorías menos frecuentes en 'Otros'.

    :param df: DataFrame a procesar.
    :param product_col: Nombre de la columna del producto original.
    :param new_col: Nombre de la nueva columna para almacenar los resultados procesados.
    :param threshold: Umbral de frecuencia para agrupar categorías menos frecuentes en 'Otros'.
    """
    if df[product_col].isna().sum() > 0:
        logger.info(f"En la columna: {product_col} se detectaron {df[product_col].isna().sum()} valores nulos")
        df[product_col] = df[product_col].fillna("NO ESPECIFICADO")
    
    # Extraer el primer segmento antes del guion y eliminar espacios
    df[new_col] = df[product_col].apply(lambda x: x.split("-")[0].strip())

    # Contar las ocurrencias de cada categoría
    counts = df[new_col].value_counts()

    # Identificar las categorías a reemplazar
    to_replace = counts[counts < threshold].index

    # Reemplazar categorías menos frecuentes por 'Otros'
    df[new_col] = df[new_col].apply(lambda x: "Otros" if x in to_replace else x)

    return df


def plot_line_weekday(
    df, date_col="fecha_apertura", title="", threshold=99, max_lines=6
):
    df[date_col] = pd.to_datetime(df[date_col])

    # Extract the day of the month and week of the year
    df["day"] = df[date_col].dt.day
    df["week"] = df[date_col].dt.isocalendar().week

    # Count the number of requests per day
    daily_counts = df.groupby("day").size()
    df_grouped = df.groupby(["subcategory", "day"]).size().unstack().fillna(0)

    # Normalize the counts to percentage
    df_grouped = (df_grouped.div(df_grouped.sum(axis=1).sum(), axis=0) * 100).round(2)

    # Apply the threshold for cumulative percentage and sort by total descending
    df_grouped = df_grouped[
        df_grouped.sum(axis=1).sort_values(ascending=False).cumsum() < threshold
    ]

    # Only keep the top 'max_lines' subcategories based on total counts
    top_subcategories = df_grouped.sum(axis=1).nlargest(max_lines).index

    # Filter the dataframe to include only the top subcategories
    df_grouped = df_grouped.loc[top_subcategories]

    # Create Plotly figure
    fig = go.Figure()

    # Add lines for each subcategory, deactivate lines after the first three
    active_subcategories = top_subcategories[:3]  # First three subcategories
    for i, subcategory in enumerate(df_grouped.index):
        fig.add_trace(
            go.Scatter(
                x=df_grouped.columns,
                y=df_grouped.loc[subcategory],
                mode="lines+markers",
                name=subcategory,
                visible="legendonly"
                if subcategory not in active_subcategories
                else True,
            )
        )

    # Add vertical lines and labels for weeks
    week_starts = df.groupby("week")["day"].min().sort_values()
    for idx, day in enumerate(week_starts):
        fig.add_vline(x=day - 1, line=dict(color="black", dash="dash"))
        if idx < len(week_starts) - 1:
            fig.add_annotation(
                x=day + 4,
                y=max(df_grouped.max()) - 1,
                text=f"Semana {idx + 1}",
                showarrow=False,
                font=dict(color="black"),
                align="center",
            )

    fig.update_layout(
        title=title,
        xaxis_title="Día del mes",
        yaxis_title="Porcentaje",
        legend_title=None,
        width=800,
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.9,  # Adjust this to place the legend below the x-axis
            xanchor="center",
            x=0.5,
            itemsizing="constant",
            traceorder="normal",
            bgcolor="rgba(255,255,255,0.7)",
        ),
        margin=dict(l=40, r=40, t=40, b=40),
    )

    return fig
