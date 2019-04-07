import { combineReducers } from 'redux';

import { authentication } from './authentication.reducer';
import { registration } from './registration.reducer';
import { users } from './users.reducer';
import { alert } from './alert.reducer';
import { groups } from './project.reducer';
import { loader } from './loader.reducer';

const rootReducer = combineReducers({
  authentication,
  registration,
  users,
  alert,
  groups,
  loader,
});

export default rootReducer;