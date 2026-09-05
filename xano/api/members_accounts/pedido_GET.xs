// Query all PEDIDO records
query pedido verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $pedido
  }

  response = $pedido
  guid = "JLzpFhMe4P6SMNzmBlvlcxgiWR0"
}