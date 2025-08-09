# Architecture Decision Record

Last edited time: November 17, 2024 7:32 PM

## PyTest - Unit Test

**Why PyTest?**

- PyTest is a widely used Python testing framework with excellent community support.
- While its simple and readable syntax makes it beginner-friendly, it is robust enough to handle complex test scenarios.
- PyTest can be integrated seamlessly into CI/CD pipelines, enabling automated test execution as part of the workflow. This ensures that any code changes are checked before deployment.
- PyTest’s efficient test discovery and execution speed make it ideal for the frequent testing cycles in a CI/CD pipeline.
- Moreover, the `pytest-cov` plugin provides test coverage metrics, allowing us to track and maintain high-quality standards over time.

**Why not others?**

- We include additional testing frameworks, such as Jest for JavaScript-based unit testing and Cypress for end-to-end testing. However, PyTest is the best choice for testing our Python backend code.
- Alternatives like Tape, Ava, and Mocha/Chai are tailored to JavaScript and Node.js environments. While they are excellent in their domain, they lack the Python-specific features and seamless integration offered by PyTest.

**Final Decision**

We chose PyTest as one of our frameworks for its simplicity, flexibility, and ability to meet the needs of our Python-based backend. Its robust features and seamless CI/CD pipeline integration ensure a reliable and efficient testing workflow.

## Codacy - Automated Code Review

**Why Codacy?**

- Codacy provides a comprehensive way to identify and address code quality issues.
- It can be integrated easily with GitHub and other version control systems, supporting our CI/CD pipeline seamlessly.
- Codacy offers test coverage metrics and can be incorporated into workflows for consistent quality checks.
- Last but not least, Codacy has a free open-source plan available for students, which aligns with our budget constraints.

**Why not others?**

- CodeClimate is an alternative for Automated Code Review, but Codacy has a simpler setup process compared to CodeClimate.
- Codacy offers clear documentation and tutorials, ensuring a smoother onboarding process for the team compared to some alternatives.
- Codacy also provides more direct and user-friendly integrations for features we prioritize, such as workflow-based test coverage and analysis, which simplifies the process for our team.

**Final Decision**

We chose Codacy for its ease of integration, comprehensive feature set, and accessibility through a free open-source plan.

## Cypress - End-to-End Test

**Why Cypress?**

- After researching, we found that it is highly recommended for end-to-end testing with a strong developer experience.
- It offers a user-friendly interface, fast execution speed, and built-in debugging tools.
- Cypress allows us to directly interact with the browser, making it easier to write and maintain tests for complex web applications.
- Works well with modern front-end frameworks, ensuring the UI of our dashboard is thoroughly tested.
- Offers straightforward GitHub Actions integration for CI/CD, with thorough tutorials available to streamline the process.

**Why not others?**

- One alternative, Selenium, requires additional setup for modern workflows, making it less convenient for our use case.
- Puppeteer is another option, effective for headless browser testing, but it lacks the comprehensive capabilities of Cypress for validating end-to-end user journeys.

**Final Decision**

We chose Cypress for its fast execution, excellent debugging features, and seamless integration with the CI/CD pipeline. Its ability to simplify complex end-to-end testing workflows while ensuring a reliable user experience makes it the ideal tool for our project.

## Jest - Unit Test

**Why Jest?**

- Its simplicity allows our team members with less experience in testing to write tests.
- It’s fast because it runs tests in parallel.
- Tutorials of different kinds (blogs, videos, etc.) are easy to find.
- It has lots of features.

**Why not others?**

- Jest does not require much configuration, while competitors like Mocha and Jasmine require additional configuration or plugins.
- Jest has native snapshot testing support, while others don’t have built-in support or they rely on third-party tools.

**Final Decision**

We chose Jest as our JavaScript unit testing framework because of its simplicity, speed, and feature-rich environment. Its native snapshot testing support, minimal configuration requirements, and abundance of tutorials make it the best fit for our project.

## ESLint - Linting

**Why ESLint?**

- It can improve our code quality by enforcing consistent code styles.
- Its customizability allows us to create or extend configurations.
- It has lots of plugins to support different frameworks and technologies.
- It integrates well with editors like VS Code for real-time linting.

**Why not others?**

- ESLint is more modern and flexible, while Linting tools like JSHint and JSLint are older and lack the support for modern JS features.
- Prettier and SonarList do not support custom rules.

**Final Decision**

We chose ESLint as our linting tool for its modern features, flexibility, and ability to enforce consistent code styles. Its support for plugins, custom configurations, and integration with popular editors like VS Code ensures that our team can maintain clean and readable code.

## GitHub Actions - CI/CD

**Why GHA?**

- It’s integrated with Github, allowing interactions with repository events like push.
- Its YAML-based configuration is simple.
- It’s free.
- It provides detailed logs for each step.

**Why not others?**

- Jenkins requires setting up a server, while GHA does not.
- As we use Github, GHA eliminates the need for external connections to repositories.

**Final Decision**

We chose GitHub Actions as our CI/CD tool due to its seamless integration with GitHub, simplicity in configuration, and cost-effectiveness. Its ability to interact directly with repository events and provide detailed logs ensures a streamlined development workflow.

## SQLite3 - Database

**Why SQLite3?**

- SQLite3 is a lightweight, embedded database that is easy to implement and requires minimal setup.
- It is serverless, so there is no need for us to run a separate database server, making deployment simpler.
- SQLite3 is highly efficient for small to medium-sized datasets and supports quick read and write operations, making it well-suited for our project’s needs.
- SQLite3 is included in Python’s standard library, making it an ideal choice for seamless integration with our Flask-based backend without the need for additional dependencies.

**Why not others?**

- One alternative that we have considered is MongoDB. However, its schema-less nature can be less ideal especially when strict data validation and consistency are needed.
- Another alternative that we have considered is PostgreSQL. However, since PostgreSQL is associated with cloud-based hosting, and for small-scale projects like ours, setting up and maintaining a server is unnecessary.

**Final Decision**

Therefore, we chose SQLite3 for its lightweight, serverless architecture, ease of implementation, and seamless integration with our Python backend.
