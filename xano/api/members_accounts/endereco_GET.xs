// Query all ENDERECO records
query endereco verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $endereco
  }

  response = $endereco
  guid = "4g50yfmknDvNOb7cIR-48A230_Y"
}