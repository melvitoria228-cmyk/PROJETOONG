// Query all STATUS_SOLCANCELAMENTO records
query status_solcancelamento verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $status_solcancelamento
  }

  response = $status_solcancelamento
  guid = "cF_iz0Nim9yS0NhAsVRnm7meYqw"
}