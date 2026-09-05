// Query all CEP records
query cep verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $cep
  }

  response = $cep
  guid = "3_jntEDLVUvNq2rOAn12HtvIQZI"
}