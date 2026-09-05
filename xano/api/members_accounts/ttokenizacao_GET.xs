// Query all TTOKENIZACAO records
query ttokenizacao verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $ttokenizacao
  }

  response = $ttokenizacao
  guid = "j9ke9aGx9WXnFSc4gmJv6bZxN2s"
}