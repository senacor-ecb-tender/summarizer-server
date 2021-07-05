# ECB Text Summarizer GUI (front-server)

INTRODUCTION:

Fronend-Application for calling text summarization backend based
on VueJS / Quasar Framework.

USAGE:

In order to use the application you have to follow these steps:

1) Login

By calling the LOGIN button you will be logged in against the backend.
The user/password is provided by Senacor team


2) Running summary task

By clicking on the button SUMMARIZE on the upper left you will
   be able to setup your summary task.
   The application will show a dialog with input fields for topic / summary length
   and an file upload component.

After entering the required data you can run the summarization task with the button SUMMARIZE
at the top of the dialog. After the backend processed your request the result will show up right to the Setup.

You can download the result by clicking button DOWNLOAD to a local txt-file.

At the right you will see a block called Rating. This use case is not implemented yet
but should be a part of a final solution. By rating every single summary result you will
build up a history of qualified training data for further improvement of
the neural network.

3) Reset setup

By clicking the button RESET the setup dialog will be reseted and you can specify
new parameters

4) Logout

WIth the button LOGOUT you can logout from the application

DEVELOPMENT:

For further development you need to install the Quasar CLI
as described within the documentation page of Quasar.

## Install the dependencies

```bash
yarn
```

### Start the app in development mode (hot-code reloading, error reporting, etc.)

```bash
quasar dev
```

### Lint the files

```bash
yarn run lint
```

### Build the app for production

```bash
quasar build
```

### Customize the configuration

See [Configuring quasar.conf.js](https://v2.quasar.dev/quasar-cli/quasar-conf-js).
