// Query all PAPEL records
query papel verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $papel
  }

  response = $papel
  guid = "6txCqqcX7mf-Q9ZejrMatG2JvvI"
}