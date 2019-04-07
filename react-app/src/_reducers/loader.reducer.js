import { loadingConstants } from '../_constants';

export function loader(state = {}, action) {
  switch (action.type) {
    case loadingConstants.LOADING:
      return {
        requesting: action.requesting,
        global: action.global
      };
    default:
      return state
  }
}