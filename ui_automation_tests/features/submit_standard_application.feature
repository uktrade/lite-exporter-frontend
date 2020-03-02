@licence @submit @all @standard
Feature: I want to indicate the standard licence I want
  As a logged in exporter
  I want to indicate the kind of licence I want
  So that I am more likely to get the correct kind of licence or the kind of licence I would like

  @LT_1091_draft @regression
  Scenario: Apply for a licence to draft and delete
    Given I go to exporter homepage and choose Test Org
    When I create a standard application
    Then I see the application overview
    When I delete the application

  @LT_1091_standard @setup @smoke
  Scenario: Submit standard application
    Given I go to exporter homepage and choose Test Org
    When I create a standard application
    And I click on the "location" section
    And I select "organisation" for where my goods are located
    And I select the site at position "1"
    And I click continue
    And I click the back link
    When I click on the "goods" section
    And I add a non-incorporated good to the application
    Then the good is added to the application
    When I click on the "end_user" section
    And I add a party of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    Then wait for download link
    When I click the back link
    And I click on the "consignee" section
    And I add a party of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    Then wait for download link
    When I click the back link
    And I click on the "notes" section
    And I add a note to the draft application
    And I submit the application
    Then application is submitted
    When I go to exporter homepage
    And I click applications
    Then I see submitted application

  @LT_1091_external @regression
  Scenario: Submit standard application with external locations and ultimate end users
    Given I go to exporter homepage and choose Test Org
    When I create a standard application
    When I click on the "goods" section
    And I add an incorporated good to the application
    Then the good is added to the application
    When I click on the "ultimate-end-users" section
    And I click on the add button
    And I add a party of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    When I upload a file "file_for_doc_upload_test_1.txt"
    Then wait for download link
    And "Delete" link is present
    When I click on the add button
    And I add a party of sub_type: "commercial", name: "Mr Jones", website: " ", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    And I remove an ultimate end user so there is one less
    Then there is only one ultimate end user
    When I click on the "location" section
    And I select "external" for where my goods are located
    And I select "new" for whether or not I want a new or existing location to be added
    And I fill in new external location form with name: "32 Lime Street", address: "London" and country: "Ukraine" and continue
    And I click on add new address
    And I fill in new external location form with name: "place", address: "1 Paris Road" and country: "Ukraine" and continue
    Then I see "2" locations
    When I click on preexisting locations
    And I select the location at position "2" in external locations list and continue
    And I click the back link
    When I click on the "end_user" section
    And I add a party of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    Then wait for download link
    When I click the back link
    And I click on the "consignee" section
    And I add a party of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    Then wait for download link
    When I click the back link
    And I submit the application
    And I click applications
    Then I see submitted application

  @LT_1074_copy_existing_party @regression
  Scenario: Submit standard application with external locations and ultimate end users and copy party
    Given I go to exporter homepage and choose Test Org
    And I create a draft
    And I seed an end user for the draft
    When I create a standard application
    And I click on the "end_user" section
    And I select that I want to copy an existing party
    When I filter for my previously created end user
    Then I can select the existing party in the table
    When I click copy party
    And I click continue
    Then I see the party name is already filled in
    When I click continue
    Then I see the party website is already filled in
    When I click continue
    Then I see the party address and country is already filled in
    When I click continue
    And I skip uploading a document
