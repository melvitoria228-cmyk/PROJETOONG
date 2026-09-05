// Query all STATUS_PEDIDO records
query status_pedido verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $status_pedido
  }

  response = $status_pedido
  guid = "zFgsmMK3L7gxIX80NRBOZLKDOJU"
}