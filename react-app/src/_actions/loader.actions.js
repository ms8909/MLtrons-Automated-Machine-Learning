import { loadingConstants } from '../_constants';

export const loaderActions = {
    requesting
};

function requesting(requesting, global=false) {
    return { type: loadingConstants.LOADING, requesting, global};
}