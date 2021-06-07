## Available Scripts

In the project directory, you can run:

_Assumes you have yarn, npm & pip installed_

### `yarn start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

Note: If you get a warning about run-p not being found
Run `npm i npm-run-all`

Required npm installs:

    npm install react
    npm install react-router-dom
    npm install d3
    npm install socket.io-client
    npm install react-dom

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

Full list of commands (UNIX-BASED OS)

    cd api
    python3 -m venv venv
    source venv/bin/activate

(Windows)

    cd api
    python -m venv venv
    venv\Scripts\activate

(Instructions shared across OS):

    pip install flask python-dotenv
    pip install numpy
    pip install flask-cors
    pip install mne
    pip install matplotlib
    pip install tensorflow
    pip install pickle
    pip install flask
    pip install flask_socketio

Simulates a local version of the backend. Run this in another terminal
window while running the front-end or the api calls won't work.
