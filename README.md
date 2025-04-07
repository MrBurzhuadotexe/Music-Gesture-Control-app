# Music Gesture Control App (Back-End)

## About

This is a **back-end** implementation of a demo showcasing **Spotify gesture controls**. It demonstrates the interaction between a web interface and Spotify using gesture controls for music playback.

### [**Front-End Demo**](https://github.com/retttddd/spotify-controls-web)

## Before Running the App

To set up the app correctly, you need to configure a few environment variables. 

1. Rename `.env.example` to `.env` in the `./src` directory.
2. Insert your **Spotify** API credentials and **backend** URL into the `.env` file:

```env
REACT_APP_REDIRECT_LINK=redirect_to_your_app
REACT_APP_CLIENT_ID=client_open_key
REACT_APP_CLIENT_SECRET=client_private_key
REACT_APP_REDIRECT_URI=endpoints_youve_entered_in_dashboard
REACT_APP_BACKEND_URL=your_backend_url
```

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.



