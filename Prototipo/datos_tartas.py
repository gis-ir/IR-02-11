tartas = {
    "red velvet": {
        "semielaborados": {
            "crema de queso": {"cantidad": 1, "materias_primas": {"queso crema": 100, "azúcar": 50}},
            "bizcocho base": {"cantidad": 1}
        },
        "materias_primas": {
            "huevos": 4,
            "harina": 200,
            "azúcar": 150
        }
    }
}

stock = {
    "semielaborados": {
        "bizcocho base": 5,  # Ya tienes 5 en stock
        "crema de queso": 0   # No tienes en stock
    },
    "materias_primas": {
        "queso crema": 50,    # Solo tienes 50g en stock
        "azúcar": 200,        # Tienes 200g en stock
        "huevos": 20,          # Solo tienes 2 huevos en stock
        "harina": 500
        # Tienes suficiente harina para 1 o 2 tartas
    }
}