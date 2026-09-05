// Get PEDIDO record
query "pedido/{pedido_id}" verb=GET {
  api_group = "Members & Accounts"

  input {
    int pedido_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.pedido_id
    } as $pedido
  
    precondition ($pedido != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $pedido
  guid = "ZWN2_1pLRyN8zAwPT0gEyMK_lNk"
}