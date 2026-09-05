// Add PEDIDO record
query pedido verb=POST {
  api_group = "Members & Accounts"

  input {
    dblink {
      table = ""
    }
  }

  stack {
    db.add "" {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $pedido
  }

  response = $pedido
  guid = "zh0FQa8vLqAJ2dJhDCMZQ8T3WDQ"
}