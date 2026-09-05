// Query all tokens records
query tokens verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $tokens
  }

  response = $tokens
  guid = "3R7UNIR6_4xpCuqN4tD8uMgQVak"
}