import { configureStore } from '@reduxjs/toolkit';
import userReducer from "./reducers.jsx";
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';

const persistConfig = {
    key: 'root',
    storage,
    // whitelist: ['user']
};

const persistedReducer = persistReducer(persistConfig, userReducer);

export const store = configureStore({
    reducer: {
        user: persistedReducer,
    },
});

export const persistor = persistStore(store);
