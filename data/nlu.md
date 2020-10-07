## intent:greet

- hey
- hello
- hi
- good morning
- good evening
- hey there


## intent:order_product

- I want to place an order.
- Hey bot help me to place an order.
- Hey bot can you help me to place order.
- Help me out to place order.
- Place order.
- I want to order.
- What all can i order?
- Place an order.
- Place an order for me.
- Help me to place order.

## intent: inform
- My name is [Aditya Aggarwal](username)
- My name is [Pratik Banka](username)
- My name is [Gaurav Garg](username)
- My name is [Tejaswini](username)
- My name is [Awais Akhtar](username)
- My name is [Kshitij Anand](username)

<!-- - [starters](dish_category)
- [meals](dish_category) -->

## regex:customer_id
- \b[A-Z]{2}-\d{3}\b
## regex:product_id
- \b[A-Z]{3}-\d{4}\b
## regex:transaction_id
- \b\d{5}\b
<!-- ## regex:any_thing
- @sys.any -->

## regex:quantity
- \b\d{1,3}\b



## intent:goodbye

- bye
- goodbye
- see you around
- see you later

## intent:affirm

- [yes](confirm)
- [indeed](confirm)
- [of course](confirm)
- that sounds good
- [correct](confirm)

## intent:deny

- no
- never
- I don't think so
- don't like that
- no way
- not really

## intent:bot_challenge

- are you a bot?
- are you a human?
- am I talking to a bot?
- am I talking to a human?


## intent:complaint_init

-I want to complain
-I have a complain
-I have an issue
-I have a problem
-I want to report an problem
-I want to report an complain
-I want to report an isssue
-complain
-I am very angry with the service.

## intent:complain

- product not delivered at time
- different colour
- deliverd wrong product
- broken product
- different product
- bad packing
- very bad quality
- bad quality
- quality not good
- bad mainenance
- unhygenic packing
- dirty packing
- [very slow delivery]{"entity": "any_thing", "role": "complaint_input"}
- [the app does not respond at all]{"entity": "any_thing", "role": "complaint_input"}
- my discount coupon did not apply
- [Product Quality](complain_type)
- [Delivery](complain_type)
- [Naaniz App](complain_type)
- [Other](complain_type)

## intent:feedback_init

-i want to give feedback
-I want to give feedback
-where to give feedback
-wat to give feedback
-I have a feedback
-I have an issue
-I have a feedback
-I want to report an feedback
-feedback


## intent:question
-[what is naaniz](faq_question)
-[how to complain](faq_question)
-[how to pay](faq_question)
-[where is naaniz located](faq_question)


## intent:faq_init

-i want to ask faq
-I want to ask faq
-where to ask faq
-wat to ask faq
-I have a faq
-I have an question
-I have a faq
-I want to report an faq
-faq

## intent:rating
-[1](rating)
-[2](rating)
-[3](rating)
-[4](rating)
-[5](rating)
-[back](rating)

## intent:faq_choice
-[1](faq_choice)
-[2](faq_choice)
-[3](faq_choice)
-[4](faq_choice)
-[5](faq_choice)
-[back2](faq_choice)

## intent:navigations
-[back](navigation)
-[back1](navigation)
-[back2](navigation)
-[back3](navigation)


## intent:query_init

-I want to query
-I have a query
-I have an issue
-I want to report an query
-I want to report queries
-query

## intent:greetback
- back
- Back
- Go back
- previous
- I want to go to home menu
- go to home
- go to home menu
- back to home
- home menu
