from rest_framework import status


def test_categorias_list_permissions(
    categorias_list_url, unauthenticatedClient, userClient, adminClient
):
    """Testa as permissões da list view de categorias"""
    unauth_res = unauthenticatedClient.get(categorias_list_url)
    assert unauth_res.status_code == status.HTTP_200_OK

    user_res = userClient.get(categorias_list_url)
    assert user_res.status_code == status.HTTP_200_OK

    admin_res = adminClient.get(categorias_list_url)
    assert admin_res.status_code == status.HTTP_200_OK


def test_categorias_create_permissions(
    categorias_list_url, unauthenticatedClient, userClient, adminClient
):
    """Testa as permissões da create view de categorias"""
    payload = {'name': 'test', 'is_instrument': False}

    unauth_res = unauthenticatedClient.post(
        categorias_list_url, payload
    )
    assert unauth_res.status_code == status.HTTP_403_FORBIDDEN

    user_res = userClient.post(categorias_list_url, payload)
    assert user_res.status_code == status.HTTP_403_FORBIDDEN

    admin_res = adminClient.post(categorias_list_url, payload)
    assert admin_res.status_code == status.HTTP_201_CREATED


def test_categorias_detail_permissions(
    categoria,
    categorias_detail_url,
    unauthenticatedClient,
    userClient,
    adminClient
):
    """Testa as permissões da detail view de categorias"""
    unauth_res = unauthenticatedClient.get(categorias_detail_url(categoria.id))
    assert unauth_res.status_code == status.HTTP_403_FORBIDDEN

    user_res = userClient.get(categorias_detail_url(categoria.id))
    assert user_res.status_code == status.HTTP_403_FORBIDDEN

    admin_res = adminClient.get(categorias_detail_url(categoria.id))
    assert admin_res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_categorias_update_permissions(
    categoria,
    categorias_detail_url,
    unauthenticatedClient,
    userClient,
    adminClient
):
    """Testa as permissões da update view de categorias"""
    payload = {'name': 'outro nome', 'is_instrument': True}

    unauth_res = unauthenticatedClient.patch(
        categorias_detail_url(categoria.id), payload
    )
    assert unauth_res.status_code == status.HTTP_403_FORBIDDEN
    unauth_res = unauthenticatedClient.put(
        categorias_detail_url(categoria.id), payload
    )
    assert unauth_res.status_code == status.HTTP_403_FORBIDDEN

    user_res = userClient.patch(
        categorias_detail_url(categoria.id), payload
    )
    assert user_res.status_code == status.HTTP_403_FORBIDDEN
    user_res = userClient.put(
        categorias_detail_url(categoria.id), payload
    )
    assert user_res.status_code == status.HTTP_403_FORBIDDEN

    admin_res = adminClient.patch(
        categorias_detail_url(categoria.id), payload
    )
    assert admin_res.status_code == status.HTTP_200_OK
    admin_res = adminClient.put(
        categorias_detail_url(categoria.id), payload
    )
    assert admin_res.status_code == status.HTTP_200_OK


def test_categorias_delete_permissions(
    categoria,
    categorias_detail_url,
    unauthenticatedClient,
    userClient,
    adminClient
):
    """Testa as permissões da delete view de categorias"""
    unauth_res = unauthenticatedClient.delete(
        categorias_detail_url(categoria.id)
    )
    assert unauth_res.status_code == status.HTTP_403_FORBIDDEN

    user_res = userClient.delete(categorias_detail_url(categoria.id))
    assert user_res.status_code == status.HTTP_403_FORBIDDEN

    admin_res = adminClient.delete(categorias_detail_url(categoria.id))
    assert admin_res.status_code == status.HTTP_204_NO_CONTENT
