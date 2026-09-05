// Query all ITEM records
query item verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $item
  }

  response = $item
  guid = "lQudHOHftkvYlEBmnHyoxYj3QhI"
}