PROMPT = """
Dada la siguiente lista de descripciones y subcategorías proporcionadas por un asesor, clasifícalas en la categoría, subcategoría y motivo apropiadas; cada descripcion solo debe tener solo una categoria, una sola subcategoria y un solo motivo que esten dentro de las listas. Lo primero que debes hacer es identificar la categoria asegurando que perteneza a la lista de categorias, luego identificar la subcategoria asegurando que pertenezca a la lista de subcategorias de la categoria identificada y finalmente identificar el motivo asegurando que pertenezca a la lista de motivos. 

Lista Descripciones y subcategorías proporcionadas por el asesor:
{descriptions_with_subcategories}

Formato de respuesta para cada ítem:
  Categoría: <category>
  Subcategoría: <subcategory>
  Motivo: <reason>

Categorías:
- Quejas
- Reclamos

Subcategorías para Quejas:
- Inconformidad en débito y gestión
- Inconformidad en el saldo y gestión cobranza
- Inconformidad Tasa Hipoteca/Leasing y venta
- Notificaciones y reclamaciones erradas
- Indemnización seguro
- Inconsistencias de pagos y compras
- Cobro errado cuotas seguros
- Mal funcionamiento de canales
- Inconformidad en la atención
- Inconformidad tarifas y comisiones
- Consulta de información
- Aclaración de información y movimiento
- Certificaciones/paz y salvos
- Estados de cuenta, extracto y reportes
- Información errada producto-servicio
- Protección de datos
- Liquidación de intereses

Subcategorías para Reclamos:
- Inconsistencias de transacciones generales
- Ajuste tasa hipoteca y asegurado
- Descuento no pago, descontento y no pago atm propio
- Pagos y recaudos mal aplicados
- Diferencia en justes saldos/intereses
- Embargos y deseembargos
- Levantamiento hipoteca
- Problemas con la Tarjeta de crédito
- Venta no abonada
- Copia de pólizas
- Acumulación/redención davipuntos-millas
- Felicitación a funcionario

Motivos:
- Certificaciones/paz y salvos
- Descuento no pago atm propio
- Extracto no generado-recibido
- Inconformidad en débito
- Atención del funcionario
- Tarjeta de Crédito
- Inconformidad venta
- Inconformidad en el saldo
- Liquidación de intereses
- Datos de la transacción
- Inconsistencia en compras
- Inconsistencia TX otras redes
- Notificaciones erradas
- Pagos mal aplicados
- Funcionamiento del canal
- Tarifas de servicio/comisiones
- Reporte o calificación
- Inconformidad gestión cobranza
- Protección de datos
- Procesos Judiciales
- Endoso póliza o cambio cia
- Info errada producto-servicio
- Ajuste tasa hipotec. Retención
- Control Solicitudes Oficina
- Acumulación davipuntos-millas
- Inconsistencia pago servicios
- Inconformidad sobre el premio
- Embargos
- Aclaración de movimiento
- Levantamiento de hipoteca
- Cobros Portal
- Cuenta bloqueada
- Tarjeta de crédito emp
- Edificios
- Estados de cuenta
- No Central Unidad cumplimiento
- Cobro errado cuotas seguros
- No Central Seguridad Bancaria
- Embargo
- Cartera Vehículo Productivo
- Prorroga cartera comercial
- Indemnización seguro
- Descuento y no pago
- Aclaración de información
- Solicitud voucher
- Diferencia intereses y/o saldo
- Copia de polizas
- Recaudos mal aplicados
- Inconformidad en débitos
- Certificaciones y Paz y Salvos
- Felicitación a funcionario
- Inconsistencia en Saldo
- Reclam. Corresponsal
- Novedades de cartera
- Ajuste valor asegurado
- Corresponsal bancario
- Inconformidad Tasa Hip/Leasing
- Exoneración de impuesto
- Inconsisten transf daviplata
- Pago mal aplicado
- Información Histórica de Pagos
- Reporte o calificación emp
- Soportes operaciones
- Detalles de la inversión
- Inconsistencia acuerdo de pago
- Aclaración Tramite
- Reporte/informe anual de costo
- Certificac. y/o paz y salvos


Ejemplo:
Descripción: "cliente indica que le ultimo adelanto no nomina no le permitio solictar el valor de los 200.000 por lo que solicto un valor de 149.000 pero al validar el sistema le etsa generando el cobro de 213.000 la valdiar los movimientos en la cuenta el ultimo uso del adelanto de nomina efectivamente esta por un valor de 149.000 por ello se solicita ajuste. Tipificacion asesor: Inconformidad en el saldo"

Por favor, proporciona las clasificaciones.

"""
