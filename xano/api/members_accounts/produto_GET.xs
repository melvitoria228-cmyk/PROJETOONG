// Query all PRODUTO records
query produto verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $produto
  }

  response = $produto
  guid = "q8adSmJSAT3WGgR4bQd_Au8YArw"
}