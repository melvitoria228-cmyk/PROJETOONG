// Query all AulaTeste records
query aulateste verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "OWVraD6mDYj_O1XUgBUxchVobcI"
}