@HMRC
Feature: I want to be able to perform actions as a HMRC user

  @LT_1008_log_in_as_hmrc_and_select_organisation_to_raise_query_for
    Scenario: Select organisation to raise query for
      # This has the second org in the seed data as a hmrc org, this is to save on multiple accesses to great sso
      Given I log into to a HMRC organisation
      When I select to raise a query for my first organisation
