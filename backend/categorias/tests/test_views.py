from rest_framework import status

from categorias.models import Categoria
from categorias.serializers import CategoriaSerializer


def test_categoria_list_view_successful(categorias_list_url, userClient):
    """Testa listagem de categorias pela api"""
    Categoria.objects.create(name='Foo', is_instrument=False)
    Categoria.objects.create(name='ABC', is_instrument=False)
    Categoria.objects.create(name='Cat1', is_instrument=True)

    res = userClient.get(categorias_list_url)
    serializer = CategoriaSerializer(
        Categoria.objects.all().order_by('name'), many=True
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data


def test_categoria_create_view_successful(categorias_list_url, adminClient):
    """Testa criação de uma categoria pela api"""
    res = adminClient.post(categorias_list_url, {'name': 'cabo'})
    cat = Categoria.objects.get(name='cabo')
    serializer = CategoriaSerializer(cat)

    assert res.status_code == status.HTTP_201_CREATED
    assert res.data == serializer.data


def test_categoria_create_view_missing_name(categorias_list_url, adminClient):
    """Testa que create view não cria uma categoria se faltar o nome"""
    res = adminClient.post(categorias_list_url, {'name': ''})

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert len(Categoria.objects.all()) == 0


def test_categoria_update_view_successful(
    categoria, categorias_detail_url, adminClient
):
    """Testa modificação de categorias pela api"""
    res = adminClient.patch(
        categorias_detail_url(categoria.id), {'name': 'novo nome'}
    )
    categoria.refresh_from_db()
    assert res.status_code == status.HTTP_200_OK
    assert categoria.name == 'novo nome'

    res = adminClient.put(
        categorias_detail_url(categoria.id), {'name': 'novissimo nome'}
    )
    categoria.refresh_from_db()
    assert res.status_code == status.HTTP_200_OK
    assert categoria.name == 'novissimo nome'


def test_categoria_update_view_missing_name(
    categoria, categorias_detail_url, adminClient
):
    """Testa que uma categoria não é modificada se faltar atributos"""
    old_name = categoria.name

    res = adminClient.patch(categorias_detail_url(categoria.id), {'name': ''})
    categoria.refresh_from_db()
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert categoria.name == old_name

    res = adminClient.put(categorias_detail_url(categoria.id), {})
    categoria.refresh_from_db()
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert categoria.name == old_name


def test_categoria_update_unexisting_id(categorias_detail_url, adminClient):
    """Testa api ao tentar modificar uma categoria que não existe"""
    res = adminClient.patch(categorias_detail_url(333), {'nome': 'novo'})
    assert res.status_code == status.HTTP_404_NOT_FOUND

    res = adminClient.put(categorias_detail_url(333), {'nome': 'novo'})
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_categoria_delete_view_successful(
    categoria, categorias_detail_url, adminClient
):
    """Testa deleção de uma categoria pela api"""
    res = adminClient.delete(categorias_detail_url(categoria.id))
    assert res.status_code == status.HTTP_204_NO_CONTENT
    assert not Categoria.objects.filter(id=categoria.id).exists()


def test_categoria_delete_view_unexisting_id(
    categorias_detail_url, adminClient
):
    """Testa aou ai tentar deletar uma categoria que não existe"""
    res = adminClient.delete(categorias_detail_url(22))
    assert res.status_code == status.HTTP_404_NOT_FOUND
