// Delete STATUS_PEDIDO record.
query "status_pedido/{status_pedido_id}" verb=DELETE {
  api_group = "Members & Accounts"

  input {
    int status_pedido_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.status_pedido_id
    }
  }

  response = null
  guid = "R5OgzPjHFW1xDwMOUIaAnc6As8E"
}