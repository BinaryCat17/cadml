import torch
from physicsnemo.sym.geometry.primitives_3d import Cylinder
from physicsnemo.sym.eq.pdes.linear_elasticity import Laplace
from physicsnemo.sym.domain import Domain
from physicsnemo.sym.domain.constraint import PointwiseConstraint
from physicsnemo.sym.models.fourier_net import FourierNetArch
from physicsnemo.sym.solver import Solver
from physicsnemo.sym.key import Key

# Параметры мотора
R_rotor = 10.0
R_stator = 10.5
height = 40.0
poles = 8

# Геометрия (analytical CSG)
rotor = Cylinder(origin=(0,0,0), radius=R_rotor, height=height, axis=(0,0,1))
stator_inner = Cylinder(origin=(0,0,0), radius=R_stator, height=height, axis=(0,0,1))
air_gap = stator_inner - rotor  # difference для зазора

# Модель (FourierNet + hybrid correction возможна через custom, но начинаем с базовой)
model = FourierNetArch(
    input_keys=[Key("x"), Key("y"), Key("z")],
    output_keys=[Key("phi")],
    nr_layers=6,
    layer_size=256
)

# PDE: Laplace ∇²phi = 0
pde = Laplace(u="phi")

# Domain
domain = Domain()

# Interior constraint (внутри зазора)
interior_constraint = PointwiseConstraint.from_geometry(
    geometry=air_gap,
    pde=pde,
    batch_size=20000
)
domain.add_constraint(interior_constraint, "interior")

# BC на роторе: периодическая намагниченность
def magnet_bc(invar):
    theta = torch.atan2(invar["y"], invar["x"])
    return torch.sin(poles * theta)

rotor_bc = PointwiseConstraint.from_geometry(
    geometry=rotor.surface,
    outvar={"phi": magnet_bc},
    batch_size=10000
)
domain.add_constraint(rotor_bc, "rotor_bc")

# Solver
solver = Solver(model=model, domain=domain)
solver.solve(max_steps=15000, accelerator="gpu")

print("Обучение завершено! Можно добавить визуализацию или экспорт.")
