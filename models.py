import db
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Boolean, Float, UniqueConstraint
from sqlalchemy import DateTime, Date
from flask_login import UserMixin
from db import Base

class User(UserMixin, db.Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    password = Column(String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Expedicion(Base):
    __tablename__ = "expedicion"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    fecha = Column(DateTime, nullable=False)
    expedicion = Column(Integer, nullable=False)
    agencia_origen = Column(String(200), nullable=False)
    agencia_destino = Column(String(200), nullable=False)
    cliente = Column(String(200), nullable=False)
    remitente = Column(String(200), nullable=False)
    dir_remitente = Column(String(200), nullable=True)
    cod_postal_remitente = Column(Integer, nullable=False)
    poblacion_remitente = Column(String(200), nullable=False)
    provincia_remitente = Column(String(200), nullable=False)
    pais_remitente = Column(String(100), nullable=False)
    tlf_remitente = Column(String(200), nullable=True)
    destinatario = Column(String(200), nullable=False)
    dir_destinatario = Column(String(200), nullable=False)
    cod_postal_destinatario = Column(Integer, nullable=False)
    poblacion_destinatario = Column(String(200), nullable=False)
    provincia_destinatario = Column(String(200), nullable=False)
    pais_destinatario = Column(String(100), nullable=False)
    tlf_destinatario = Column(String(200), nullable=True)
    bultos = Column(Integer, nullable=False)
    kg = Column(Integer, nullable=False)
    volumen = Column(Float, nullable=True)
    kg_conv = Column(Integer, nullable=False)
    tipo_bulto = Column(String(100), nullable=True)
    reembolso = Column(Float, nullable=True, default=0.0)
    estado = Column(Enum("almacen", "en reparto", "entregado", name="estado_expedicion"), nullable=False,
                    default="almacen")
    fecha_asignacion = Column(DateTime, nullable=True)
    fecha_entrega = Column(DateTime, nullable=True)
    facturada = Column(Boolean, default=False)
    asignada_a = Column(String, default=True)
    viaje = Column(Integer, nullable=True)
    ingreso_com_reembolso = Column(Float, nullable=True, default=0.0)
    ingreso_distribucion = Column(Float, nullable=True, default=0.0)
    ingreso_cargo_adicional = Column(Float, nullable=True, default=0.0)
    coste_reparto = Column(Float, nullable=True, default=0.0)
    coste_arrastre = Column(Float, nullable=True, default=0.0)
    coste_removido = Column(Float, nullable=True, default=0.0)
    coste_distribucion = Column(Float, nullable=True, default=0.0)
    albaran_entrega = Column(Boolean, default=False)
    albaran_cliente = Column(Boolean, default=False)
    observaciones = Column(String(200), nullable=True)
    incidencia_tipo = Column(Enum("ausente", "rechazado", "sin tiempo", "0", name="incidencia_tipo"), nullable=True,
                    default="0")
    fecha_incidencia = Column(DateTime, nullable=True)
    incidencia_ampliacion = Column(String(200), nullable=True)
    dev_alb_firmado = Column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint('expedicion', 'cliente', name='_expedicion_cliente_uc'),
    )

    def __init__(self, fecha, expedicion, agencia_origen, agencia_destino, cliente, remitente, dir_remitente,
                 cod_postal_remitente,
                 poblacion_remitente, provincia_remitente, pais_remitente, destinatario, dir_destinatario,
                 cod_postal_destinatario, poblacion_destinatario, provincia_destinatario, pais_destinatario, bultos, kg,
                 volumen=0, kg_conv=kg, incidencia_tipo=None, incidencia_ampliacion=None,
                 tipo_bulto=None, reembolso=0.0, estado="almacen", facturada=False, asignada_a=None, viaje=None,
                 fecha_asignacion=None, fecha_entrega=None, fecha_incidencia = None,
                 ingreso_com_reembolso=0.0, ingreso_distribucion=0.0, ingreso_cargo_adicional=0.0, coste_reparto=0.0,
                 coste_arrastre=0.0, coste_removido=0.0,dev_alb_firmado=False,
                 coste_distribucion=0.0, tlf_remitente=0, tlf_destinatario=0, albaran_entrega=False, albaran_cliente=False, observaciones=None):
        self.fecha = fecha
        self.expedicion = expedicion
        self.agencia_origen = agencia_origen
        self.agencia_destino = agencia_destino
        self.cliente = cliente
        self.remitente = remitente
        self.dir_remitente = dir_remitente
        self.cod_postal_remitente = cod_postal_remitente
        self.poblacion_remitente = poblacion_remitente
        self.provincia_remitente = provincia_remitente
        self.pais_remitente = pais_remitente
        self.destinatario = destinatario
        self.dir_destinatario = dir_destinatario
        self.cod_postal_destinatario = cod_postal_destinatario
        self.poblacion_destinatario = poblacion_destinatario
        self.provincia_destinatario = provincia_destinatario
        self.pais_destinatario = pais_destinatario
        self.bultos = bultos
        self.kg = kg
        self.volumen = volumen
        self.kg_conv = kg
        self.tipo_bulto = tipo_bulto
        self.reembolso = reembolso
        self.estado = estado
        self.facturada = facturada
        self.asignada_a = asignada_a
        self.viaje = viaje
        self.fecha_asignacion = fecha_asignacion
        self.fecha_entrega = fecha_entrega
        self.ingreso_com_reembolso = ingreso_com_reembolso
        self.ingreso_distribucion = ingreso_distribucion
        self.ingreso_cargo_adicional = ingreso_cargo_adicional
        self.coste_reparto = coste_reparto
        self.coste_arrastre = coste_arrastre
        self.coste_removido = coste_removido
        self.coste_distribucion = coste_distribucion
        self.tlf_remitente = tlf_remitente
        self.tlf_destinatario = tlf_destinatario
        self.albaran_cliente = albaran_cliente
        self.albaran_entrega = albaran_entrega
        self.observaciones = observaciones
        self.incidencia_tipo = incidencia_tipo
        self.incidencia_ampliacion = incidencia_ampliacion
        self.dev_alb_firmado = dev_alb_firmado
        self.fecha_incidencia = fecha_incidencia

    def __str__(self):
        return (
            f"Expedición {self.expedicion}:\n"
            f"Fecha: {self.fecha}\n"
            f"Agencia Origen: {self.agencia_origen}, Agencia Destino: {self.agencia_destino}\n"
            f"Cliente: {self.cliente}\n"
            f"Remitente: {self.remitente}, Dirección: {self.dir_remitente}, "
            f"CP: {self.cod_postal_remitente}, Población: {self.poblacion_remitente}, "
            f"Provincia: {self.provincia_remitente}, País: {self.pais_remitente}\n"
            f"Destinatario: {self.destinatario}, Dirección: {self.dir_destinatario}, "
            f"CP: {self.cod_postal_destinatario}, Población: {self.poblacion_destinatario}, "
            f"Provincia: {self.provincia_destinatario}, País: {self.pais_destinatario}\n"
            f"Bultos: {self.bultos}, Peso: {self.kg} kg, Volumen: {self.volumen} m³, KG Conv: {self.kg_conv}\n"
            f"Estado: {self.estado}, Reembolso: {self.reembolso}€\n"
            f"Fecha Asignación: {self.fecha_asignacion}, Fecha Entrega: {self.fecha_entrega}, Viaje: {self.viaje}\n"
            f"Ingresos - Com Reembolso: {self.ingreso_com_reembolso}€, Distribución: {self.ingreso_distribucion}€, "
            f"Cargo Adicional: {self.ingreso_cargo_adicional}€\n"
            f"Costes - Reparto: {self.coste_reparto}€, Arrastre: {self.coste_arrastre}€, "
            f"Removido: {self.coste_removido}€, Distribución: {self.coste_distribucion}€"
        )

class Agencias(Base):
    __tablename__ = "agencias"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre_comercial = Column(String(200), nullable=False)
    nombre_fiscal = Column(String(200), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

    def __init__(self, nombre_comercial, nombre_fiscal, activo=True):
        self.nombre_comercial = nombre_comercial
        self.nombre_fiscal = nombre_fiscal
        self.activo = activo

    def __str__(self):
        return f"Agencia: {self.nombre_comercial} ({'Activo' if self.activo else 'Inactivo'})"



class Cliente(Base):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    alias = Column(String(200), nullable=False)
    nombre_fiscal = Column(String(200), nullable=False)
    direccion = Column(String(200), nullable=True)
    codigo_postal = Column(Integer, nullable=True)
    poblacion = Column(String(200), nullable=True)
    provincia = Column(String(200), nullable=True)
    pais = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    telefono = Column(Integer, nullable=True)
    tarifa = Column(String(100), nullable=True)
    notas = Column(String(300), nullable=True)
    activo = Column(Boolean, default=True, nullable=False)

    def __init__(self, alias, nombre_fiscal, direccion=None, codigo_postal=None, poblacion=None, provincia=None, pais=None, email=None, telefono=None, tarifa=None, notas =None, activo=True):
        self.alias = alias
        self.nombre_fiscal = nombre_fiscal
        self.direccion = direccion
        self.codigo_postal = codigo_postal
        self.poblacion = poblacion
        self.provincia = provincia
        self.pais = pais
        self.email = email
        self.telefono = telefono
        self.notas = notas
        self.activo = activo
        self.tarifa = tarifa

    def __str__(self):
        return f"Cliente: {self.alias} ({'Activo' if self.activo else 'Inactivo'})"

class Vehiculo(Base):
    __tablename__ = "vehiculo"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    matricula = Column(String(20), unique=True, nullable=False)
    alias = Column(String(20), nullable=True)
    capacidad = Column(Integer, nullable=False)
    caducidad_itv = Column(Date, nullable=True)
    caducidad_seguro = Column(Date, nullable=True)
    caducidad_tacografo = Column(Date, nullable=True)
    chofer_habitual = Column(String(200), nullable=True)
    activo = Column(Boolean, default=True, nullable=False)

    def __init__(self, matricula,alias=None, capacidad=0, caducidad_itv="99/99/9999 00:00:00", caducidad_seguro=None, caducidad_tacografo=None, chofer_habitual=None, activo=True):
        self.matricula = matricula
        self.capacidad = capacidad
        self.caducidad_itv = caducidad_itv
        self.caducidad_seguro = caducidad_seguro
        self.caducidad_tacografo = caducidad_tacografo
        self.chofer_habitual = chofer_habitual
        self.activo = activo
        self.alias = alias

    def __str__(self):
        return f"Vehículo: {self.matricula} ({'Activo' if self.activo else 'Inactivo'})"
