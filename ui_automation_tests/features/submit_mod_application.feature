@licence @submit @all @MOD
Feature: I want to create MOD Licence Applications
  As a logged in exporter
  I want to apply for an MOD clearance for equipment or information if I need one
  So that I can get approval to provide the relevant equipment or information to a third party outside the UK

  @LT_1169_exhibition_clearance @setup @smoke
  Scenario: Submit Exhibition Clearance Application
    Given I go to exporter homepage and choose Test Org
    When I select a licence of type "mod"
    And I select a MOD licence of type "exhc"
    And I enter a licence name
    Then I see my edited reference name
    When I click on the "location" section
    And I select "organisation" for where my goods are located
    And I select the site at position "1"
    And I click continue
    And I click the back link
    When I click on the "goods" section
    And I add a non-incorporated good to the application
    Then the good is added to the application
    When I click on the "end_user" section
    And I add an party of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    Then wait for download link
    When I click the back link
    And I click on the "consignee" section
    And I add an party of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    Then wait for download link
    When I click the back link
    And I submit the application
    Then application is submitted
    When I go to exporter homepage
    And I click applications
    Then I see submitted application

  @LT_1980_MOD_clearance @setup @smoke
  Scenario: Submit F680 Application
    Given I go to exporter homepage and choose Test Org
    When I select a licence of type "mod"
    And I select a MOD licence of type "f680"
    And I enter a licence name
    When I click on the "clearance" section
    And I choose a clearance level for my application
    And I click on the "goods" section
    And I add a non-incorporated good to the application
    Then the good is added to the application
    When I click on the "end_user" section
    And I add an end user with clearance of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", clearance: "uk_unclassified", address: "London" and country "Ukraine"
    And I click continue
    And I upload a file "file_for_doc_upload_test_1.txt"
    Then wait for download link
    When I click the back link
    And I submit the application
    Then application is submitted
    When I go to exporter homepage
    And I click applications
    Then I see submitted application

  @LT_1980_gifting_clearance @setup @smoke
  Scenario: Submit Gifting Application
    Given I go to exporter homepage and choose Test Org
    When I select a licence of type "mod"
    And I select a MOD licence of type "gift"
    And I enter a licence name
    When I click on the "goods" section
    And I add a non-incorporated good to the application
    Then the good is added to the application
    When I click on the "end_user" section
    And I add an party of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    Then wait for download link
    When I click the back link
    And I submit the application
    Then application is submitted
    When I go to exporter homepage
    And I click applications
    Then I see submitted application
