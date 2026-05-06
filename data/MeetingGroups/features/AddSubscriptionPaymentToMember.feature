Feature: Add Subscription Payment To Member

    Background:
      Given there is a UserAccess system
      And there is a Administration system
      And there is a Meetings system
      And there is a Payments system
      And there is a member with id 1
      And there is a member with id 2
      And the current system date is "2025-12-01"

    Scenario: Successfully add a subscription payment until the end of the month
      When a subscription payment is added to member 1 with value 10.00, currency "CAD", and subscriptionPeriod "Month"
      Then the system shall not throw an error
      Then the number of subscription payments shall be 1
      Then the subscription payment 1 payer shall be member 1
      Then the subscription payment 1 countryCode shall be "ca"
      Then the subscription payment 1 subscriptionPeriod shall be "Month"
      Then the subscription payment 1 status shall be "WaitingForPayment"
      Then the subscription payment 1 value shall be 10.00
      Then the subscription payment 1 currency shall be "CAD"
      Then the number of subscriptions shall be 1
      Then the subscription 1 member shall be member 1
      Then the subscription 1 countryCode shall be "ca"
      Then the subscription 1 expirationDate shall be "2025-12-31"
      Then the subscription 1 subscriptionPeriod shall be "Month"
      Then the subscription 1 status shall be "Active"

    Scenario: Successfully add a subscription payment for 6 months
      When a subscription payment is added to member 1 with value 50.00, currency "CAD", and subscriptionPeriod "HalfYear"
      Then the system shall not throw an error
      Then the number of subscription payments shall be 1
      Then the subscription payment 1 payer shall be member 1
      Then the subscription payment 1 countryCode shall be "ca"
      Then the subscription payment 1 subscriptionPeriod shall be "HalfYear"
      Then the subscription payment 1 status shall be "WaitingForPayment"
      Then the subscription payment 1 value shall be 50.00
      Then the subscription payment 1 currency shall be "CAD"
      Then the number of subscriptions shall be 1
      Then the subscription 1 member shall be member 1
      Then the subscription 1 countryCode shall be "ca"
      Then the subscription 1 expirationDate shall be "2026-05-31"
      Then the subscription 1 subscriptionPeriod shall be "HalfYear"
      Then the subscription 1 status shall be "Active"

    Scenario: Unsuccessfully add a subscription payment to a member with an existing subscription
      Given the following subscriptions exist:
          | memberId | countryCode | expirationDate | subscriptionPeriod | status |
          | 1        | ca          | 2025-12-31     | Month              | Active |
      When a subscription payment is added to member 1 with value 10.00, currency "CAD", and subscriptionPeriod "Month"
      Then the system shall throw with error message "Member already has a subscription."
      Then the number of subscription payments shall be 0

    Scenario: Unsuccessfully add a subscription payment to a non-existent member
      When a subscription payment is added to member 999 with value 10.00, currency "CAD", and subscriptionPeriod "Month"
      Then the system shall throw with error message "Member does not exist."
      Then the number of subscription payments shall be 0

    Scenario: Unsuccessfully add a subscription payment to a member with an expired subscription
      Given the following subscriptions exist:
        | memberId | countryCode | expirationDate | subscriptionPeriod | status  |
        | 2        | ca          | 2025-10-30     | Month              | Expired |
      When a subscription payment is added to member 2 with value 10.00, currency "CAD", and subscriptionPeriod "Month"
      Then the system shall throw with error message "Member already has a subscription."
      Then the number of subscription payments shall be 0

    Scenario Outline: Unsuccessfully add a subscription payment with invalid values
        When a subscription payment is added to member 1 with value <value>, currency "<currency>", and subscriptionPeriod "<subscriptionPeriod>"
        Then the system shall throw with error message "<errorMessage>"
        Then the number of subscription payments shall be 0

        Examples:
          | value  | currency | subscriptionPeriod | errorMessage                              |
          | -10.00 | CAD      | Month              | The value must be positive.               |
          | 0.00   | CAD      | Month              | The value must be positive.               |
          | 10.00  |          | Month              | The currency must not be empty.           |
          | 10.00  | CAD      |                    | The subscriptionPeriod must not be empty. |
