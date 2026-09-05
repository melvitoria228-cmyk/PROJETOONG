// Query all user records
query user verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $user
  }

  response = $user
  guid = "nwtQZhTPbU6Z6E0NyEYgW7ROnWo"
}