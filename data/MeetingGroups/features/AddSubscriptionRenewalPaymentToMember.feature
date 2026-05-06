Feature: Add Subscription Renewal Payment To Member

    Background:
        Given there is a UserAccess system
        And there is a Administration system
        And there is a Meetings system
        And there is a Payments system
        And there is a member with id 1
        And there is a member with id 2
        And the current system date is "2025-12-01"
        And the following subscriptions exist:
            | memberId | countryCode | expirationDate | subscriptionPeriod | status |
            | 1        | ca          | 2025-12-31     | Month              | Active |

    Scenario: Successfully add a subscription renewal payment to a member
        When a subscription renewal payment is added to member 1 with value 10.00 and currency "CAD"
        Then the system shall not throw an error
        Then the number of subscription renewal payments shall be 1
        Then the subscription renewal payment 1 payer shall be member 1
        Then the subscription renewal payment 1 countryCode shall be "ca"
        Then the subscription renewal payment 1 subscriptionPeriod shall be "Month"
        Then the subscription renewal payment 1 status shall be "WaitingForPayment"
        Then the subscription renewal payment 1 value shall be 10.00
        Then the subscription renewal payment 1 currency shall be "CAD"

    Scenario: Successfully add multiple subscription renewal payments to a member
        When a subscription renewal payment is added to member 1 with value 10.00 and currency "CAD"
        And a subscription renewal payment is added to member 1 with value 20.00 and currency "CAD"
        Then the system shall not throw an error
        Then the number of subscription renewal payments shall be 2
        Then the subscription renewal payment 1 payer shall be member 1
        Then the subscription renewal payment 1 countryCode shall be "ca"
        Then the subscription renewal payment 1 subscriptionPeriod shall be "Month"
        Then the subscription renewal payment 1 status shall be "WaitingForPayment"
        Then the subscription renewal payment 1 value shall be 10.00
        Then the subscription renewal payment 1 currency shall be "CAD"
        Then the subscription renewal payment 2 payer shall be member 1
        Then the subscription renewal payment 2 countryCode shall be "ca"
        Then the subscription renewal payment 2 subscriptionPeriod shall be "Month"
        Then the subscription renewal payment 2 status shall be "WaitingForPayment"
        Then the subscription renewal payment 2 value shall be 20.00
        Then the subscription renewal payment 2 currency shall be "CAD"

    Scenario: Unsuccessfully add a subscription renewal payment to a member without a subscription
        When a subscription renewal payment is added to member 2 with value 10.00 and currency "CAD"
        Then the system shall throw with error message "Member does not have a subscription."
        Then the number of subscription renewal payments shall be 0

    Scenario: Unsuccessfully add a subscription renewal payment to a non-existent member
        When a subscription renewal payment is added to member 999 with value 10.00 and currency "CAD"
        Then the system shall throw with error message "Member does not exist."
        Then the number of subscription renewal payments shall be 0

    Scenario: Unsuccessfully add a subscription renewal payment with a member with expired subscription
        Given the following subscriptions exist:
            | memberId | countryCode | expirationDate | subscriptionPeriod | status  |
            | 2        | ca          | 2025-10-30     | Month              | Expired |
        When a subscription renewal payment is added to member 2 with value 10.00 and currency "CAD"
        Then the system shall throw with error message "Member does not have an active subscription."
        Then the number of subscription renewal payments shall be 0

    Scenario Outline: Unsuccessfully add a subscription renewal payment with invalid values
        When a subscription renewal payment is added to member 1 with value <value> and currency "<currency>"
        Then the system shall throw with error message "<errorMessage>"
        Then the number of subscription renewal payments shall be 0

        Examples:
            | value  | currency | errorMessage                    |
            | -10.00 | CAD      | The value must be positive.     |
            | 0.00   | CAD      | The value must be positive.     |
            | 10.00  |          | The currency must not be empty. |
