@end_user_advisory_queries @all
Feature:

  @LT_1007
    @MSTG
  Scenario: create and see listed an end user advisory
    Given I go to exporter homepage and choose Test Org
    When I click on end user advisories
    And I select to create a new advisory
    And I select "government" option and continue
    And I select "John" for the name, "4 place" for the address, "Aruba" as the country, and continue
    And I enter "reasoning" for my reason, and "these are notes" for notes and click submit
    Then I am given a confirmed submitted page, and am shown a 10 digit code
