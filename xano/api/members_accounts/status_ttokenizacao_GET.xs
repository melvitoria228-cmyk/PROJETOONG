// Query all STATUS_TTOKENIZACAO records
query status_ttokenizacao verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $status_ttokenizacao
  }

  response = $status_ttokenizacao
  guid = "jujIWqkqgS0RHpciplthAXMXMZc"
}