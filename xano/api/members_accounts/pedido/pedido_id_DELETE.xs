// Delete PEDIDO record.
query "pedido/{pedido_id}" verb=DELETE {
  api_group = "Members & Accounts"

  input {
    int pedido_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.pedido_id
    }
  }

  response = null
  guid = "52jBAnH86hHP1sqk69KB5MIMdzc"
}