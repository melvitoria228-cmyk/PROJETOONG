// Query all OP records
query op verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $op
  }

  response = $op
  guid = "j7UGu3LBrXb7dI_nI0oonDBYF6M"
}