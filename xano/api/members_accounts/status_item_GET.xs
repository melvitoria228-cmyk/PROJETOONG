// Query all STATUS_ITEM records
query status_item verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $status_item
  }

  response = $status_item
  guid = "Bun0ZK0s8Yan19FvmCL9lTDmtrU"
}