# Instructions for local development (e.g. Peer Review)

**Before you begin**: Make sure to have `npm` and `yarn` installed on your machine, 
as well as way to create Python virtual environments.

1. Clone repo and cd into `seizure-classification` directory.
2. Create Python virtual environment using Python version 3.7 (we recommend conda).
3. Activate the virtual environment.
4. Install Python dependencies by running `pip install -r requirements.txt`
5. Ensure front end dependencies up-to-date by running `yarn install`

Setup is now complete! You may test our tool by using the following steps:
1. Open two terminal windows.
2. In the first window, run `yarn start`. This will open our front end on localhost.
3. In the second window, run `yarn start-api`. This will run our back end on localhost and enable api calls.
4. Choose an `.edf` file for upload. Try the file in our `sample_data` folder.
5. Click the `Upload data` button and watch the prediction probabilities of seizure appear in the web browser!

## Available Scripts

In the project directory, you can run:

### `yarn start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `yarn test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `yarn build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `yarn eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

### `yarn start-api`

_Assumes python3 installed_
Simulates a local version of the backend. Run this in another terminal
window while running the front-end or the api calls won't work.
