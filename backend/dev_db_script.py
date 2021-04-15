from equipamentos.models import Equipamento
from categorias.models import Categoria

# Limpa DB
for cat in Categoria.objects.all():
    cat.delete()
for equip in Equipamento.objects.all():
    equip.delete()


# Cria categorias
cat_corda = Categoria.objects.create(name='Corda')
cat_sopro = Categoria.objects.create(name='Sopro')
cat_bateria = Categoria.objects.create(name='Bateria')

cat_amp = Categoria.objects.create(name='Amplificador')
cat_cabo = Categoria.objects.create(name='Cabo')
cat_pedal = Categoria.objects.create(name='Pedal')
cat_mesa = Categoria.objects.create(name='Mixing Table')


# Cria instrumentos
e = Equipamento.objects.create(
    name="Violão",
    description="Lorem Ipsum",
    price_per_day=8.00,
    is_instrument=True,
    image="equipaments/violao.jpg",
)
e.categorias.add(cat_corda)

e = Equipamento.objects.create(
    name="Guitarra",
    description="Lorem Ipsum",
    price_per_day=12.00,
    is_instrument=True,
    image="equipaments/guitar.jpg",
)
e.categorias.add(cat_corda)

e = Equipamento.objects.create(
    name="Ukulele",
    description="Lorem Ipsum",
    price_per_day=6.99,
    is_instrument=True,
    image="equipaments/ukulele.jpg",
)
e.categorias.add(cat_corda)

e = Equipamento.objects.create(
    name="Bateria simples",
    description="Lorem Ipsum",
    price_per_day=13.5,
    is_instrument=True,
    image="equipaments/drums.jpg",
)
e.categorias.add(cat_bateria)

e = Equipamento.objects.create(
    name="Bateria completa",
    description="Lorem Ipsum",
    price_per_day=24.99,
    is_instrument=True,
    image="equipaments/drums2.jpg",
)
e.categorias.add(cat_bateria)

e = Equipamento.objects.create(
    name="Saxofone",
    description="Lorem Ipsum",
    price_per_day=14.2,
    is_instrument=True,
    image="equipaments/sax.jpg",
)
e.categorias.add(cat_sopro)

e = Equipamento.objects.create(
    name="Clarinete",
    description="Lorem Ipsum",
    price_per_day=15.0,
    is_instrument=True,
    image="equipaments/clarinet.jpg",
)
e.categorias.add(cat_sopro)


# Cria equipamentos
e = Equipamento.objects.create(
    name="Amplificador modelo 1",
    description="Lorem Ipsum",
    price_per_day=13.5,
    is_instrument=False,
    image="equipaments/amp.jpg",
)
e.categorias.add(cat_amp)

e = Equipamento.objects.create(
    name="Amplificador modelo 2",
    description="Lorem Ipsum",
    price_per_day=16.8,
    is_instrument=False,
    image="equipaments/amp2.jpg",
)
e.categorias.add(cat_amp)

e = Equipamento.objects.create(
    name="Pedaleira para guitarra",
    description="Lorem Ipsum",
    price_per_day=4.5,
    is_instrument=False,
    image="equipaments/pedal.jpg",
)
e.categorias.add(cat_pedal)

e = Equipamento.objects.create(
    name="Mesa de som",
    description="Lorem Ipsum",
    price_per_day=31.2,
    is_instrument=False,
    image="equipaments/mixing_table.jpg",
)
e.categorias.add(cat_mesa)

