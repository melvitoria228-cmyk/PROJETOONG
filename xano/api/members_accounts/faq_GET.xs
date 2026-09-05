// Query all FAQ records
query faq verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $faq
  }

  response = $faq
  guid = "XAsHr53uCFvjg4LI7OlXUyju0cM"
}