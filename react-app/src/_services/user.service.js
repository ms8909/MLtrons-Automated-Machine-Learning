import config from 'config';
import { authHeader } from '../_helpers';

function fetchProgress(url, opts={}, onProgress) {
    return new Promise( (res, rej)=>{
        var xhr = new XMLHttpRequest();
        xhr.open(opts.method || 'get', url);
        for (var k in opts.headers||{})
            xhr.setRequestHeader(k, opts.headers[k]);
        xhr.onload = e => res(e.target.responseText);
        xhr.onerror = rej;
        if (xhr.upload && onProgress)
            xhr.upload.onprogress = onProgress; // event.loaded / event.total * 100 ; //event.lengthComputable
        xhr.send(opts.body);
    });
}


export const userService = {
    login,
    logout,
    register,
    getAll,
    getById,
    update,
    getTags,
    getDurations,
    addGroup,
    delete: _delete,
    searchTag,
    allGroups,
    filterGroups,
    getGroupById,
    getMembersGroupById,
    getChatsGroupById,
    addChat,
    getGroupByUserId,
    getUsers,
    getJobTitles,
    addTag,
    addMemeber,
    promoteMember,
    deleteMember,
    fb_login,
    google_login,
    getProjects,
    addProject,
    deleteProject,
    getProject,
    addDataset,
    deleteDataset,
    getMeta,
    getType,
    getRole,
    getImputation,
    updateMeta,
    addConnection,
    deleteConnection,
    getMetaConnections,
    getDatasetData,
    getProblemType,
    createTraining,
    getTrainingDetail,
    getTrainingMetric,
    getTrainingModels,
    getAccuracy,
    getBluePrint,
    getROC,
    getLossInteraction,
    getActualPrediction,
    getFeatureImportance,
    mergeConnections,
    getTimeType,
    deployModel,
    getDeployedModel,
    addTesting,
    getTestingData,
    startTesting,
    getTestingGraph,
    getTaskProgress,
    filterTrainingModels,
    interruptTraining,
    updateLoc
};

function login(email, password) {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    };
    return fetch(`${config.apiUrl}/account/auth/login/`, requestOptions)
        .then(handleResponse)
        .then(user => {
            // login successful if there's a jwt token in the response
            if (user.token) {
                // store user details and jwt token in local storage to keep user logged in between page refreshes
                localStorage.setItem('user', JSON.stringify(user));
            }

            return user;
        });
}

function fb_login(access_token) {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ access_token })
    };

    return fetch(`${config.apiUrl}/accounts/auth/facebook/`, requestOptions)
        .then(handleResponse)
        .then(user => {
            // login successful if there's a jwt token in the response
            if (user.token) {
                // store user details and jwt token in local storage to keep user logged in between page refreshes
                localStorage.setItem('user', JSON.stringify(user));
            }

            return user;
        });
}

function google_login(access_token) {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ access_token })
    };

    return fetch(`${config.apiUrl}/accounts/auth/google/`, requestOptions)
        .then(handleResponse)
        .then(user => {
            // login successful if there's a jwt token in the response
            if (user.token) {
                // store user details and jwt token in local storage to keep user logged in between page refreshes
                localStorage.setItem('user', JSON.stringify(user));
            }

            return user;
        });
}


function logout() {
    // remove user from local storage to log user out
    localStorage.removeItem('user');
}

function getAll() {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };

    return fetch(`${config.apiUrl}/users`, requestOptions).then(handleResponse);
}


function getTags() {
    const requestOptions = {
        method: 'GET',
    };
    return fetch(`${config.apiUrl}/apis/tags/`, requestOptions).then(handleResponse);
}

function getUsers() {
    const requestOptions = {
        method: 'GET',
    };
    return fetch(`${config.apiUrl}/apis/users/`, requestOptions).then(handleResponse);
}

function getJobTitles() {
    const requestOptions = {
        method: 'GET',
    };
    return fetch(`${config.apiUrl}/apis/job-titles/`, requestOptions).then(handleResponse);
}

function addMemeber(member) {
    let header = { 'Content-Type': 'application/json' }
    const requestOptions = {
        method: 'POST',
        headers: {...header, ...authHeader()},
        body: JSON.stringify(member)
    };

    return fetch(`${config.apiUrl}/apis/members/`, requestOptions).then(handleResponse);
}

function promoteMember(id) {
    let header = { 'Content-Type': 'application/json' }
    const requestOptions = {
        method: 'GET',
        headers: {...header, ...authHeader()},
    };
    return fetch(`${config.apiUrl}/apis/members/${id}/promote/`, requestOptions).then(handleResponse);
}

function deleteMember(id) {
    let header = { 'Content-Type': 'application/json' }
    const requestOptions = {
        method: 'DELETE',
        headers: {...header, ...authHeader()},
    };
    return fetch(`${config.apiUrl}/apis/members/${id}/`, requestOptions).then(handleResponse);
}

function addTag(group) {
    let header = { 'Content-Type': 'application/json' }
    const requestOptions = {
        method: 'POST',
        headers: {...header, ...authHeader()},
        body: JSON.stringify(group)
    };

    return fetch(`${config.apiUrl}/apis/tags/`, requestOptions).then(handleResponse);
}

function getDurations() {
    const requestOptions = {
        method: 'GET',
    };
    return fetch(`${config.apiUrl}/apis/durations/`, requestOptions).then(handleResponse);
}


function searchTag(search) {
    const requestOptions = {
        method: 'GET',
    };
    return fetch(`${config.apiUrl}/apis/tags/search-tag/?t_s=`+search, requestOptions).then(handleResponse);
}

function addGroup(group) {
    let header = { 'Content-Type': 'application/json' }
    const requestOptions = {
        method: 'POST',
        headers: {...header, ...authHeader()},
        body: JSON.stringify(group)
    };

    return fetch(`${config.apiUrl}/apis/groups/`, requestOptions).then(handleResponse);
}

function allGroups() {
    let header = { 'Content-Type': 'application/json' }
    const requestOptions = {
        method: 'GET',
        headers: {...header, ...authHeader()},
    };
    return fetch(`${config.apiUrl}/apis/groups/`, requestOptions).then(handleResponse);
}


function filterGroups(tags) {
    let header = { 'Content-Type': 'application/json' }
    const requestOptions = {
        method: 'POST',
        headers: {...header, ...authHeader()},
        body: JSON.stringify({
            'tags': tags
        })
    };
    return fetch(`${config.apiUrl}/apis/groups/by-tags/`, requestOptions).then(handleResponse);
}


function getGroupById(id) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/groups/${id}`, requestOptions).then(handleResponse);
}

function getGroupByUserId(id) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/groups/${id}/by-user/`, requestOptions).then(handleResponse);
}



function getMembersGroupById(id) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/members/${id}/by-group`, requestOptions).then(handleResponse);
}

function getChatsGroupById(id) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/chats/${id}/by-group`, requestOptions).then(handleResponse);
}


function getchatByGroupId(id) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/groups/${id}`, requestOptions).then(handleResponse);
}


function getById(id) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };

    return fetch(`${config.apiUrl}/users/${id}`, requestOptions).then(handleResponse);
}


function register(user) {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(user)
    };

    return fetch(`${config.apiUrl}/account/auth/register/`, requestOptions).then(handleResponse);
}

function addChat(user) {
    let header = { 'Content-Type': 'application/json' }
    const requestOptions = {
        method: 'POST',
        headers: {...header, ...authHeader()},
        body: JSON.stringify(user)
    };
    return fetch(`${config.apiUrl}/apis/chats/`, requestOptions).then(handleResponse);
}

function update(user) {
    const requestOptions = {
        method: 'PUT',
        headers: { ...authHeader(), 'Content-Type': 'application/json' },
        body: JSON.stringify(user)
    };

    return fetch(`${config.apiUrl}/users/${user.id}`, requestOptions).then(handleResponse);;
}

// prefixed function name with underscore because delete is a reserved word in javascript
function _delete(id) {
    const requestOptions = {
        method: 'DELETE',
        headers: authHeader()
    };

    return fetch(`${config.apiUrl}/users/${id}`, requestOptions).then(handleResponse);
}

function handleResponse(response) {
    return response.text().then(text => {
        const data = text && JSON.parse(text);
        if (!response.ok) {
            if (response.status === 401) {
                // auto logout if 401 response returned from api
                logout();
                location.reload(true);
            }

            const error = (data && data.message) || response.statusText;
            return Promise.reject(error);
        }

        return data;
    });
}

function getProjects() {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };

    return fetch(`${config.apiUrl}/apis/project/`, requestOptions).then(handleResponse);
}

function getTrainingDetail(id) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/training/${id}/by-project/`, requestOptions).then(handleResponse);
}

function getTrainingModels(id) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/models/${id}/by-training/`, requestOptions).then(handleResponse);
}

function filterTrainingModels(id, metric) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/models/${id}/by-rank/?metric=${metric}`, requestOptions).then(handleResponse);
}

function getAccuracy(id, project_id) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/models/${id}/accuracy/?project=${project_id}`, requestOptions).then(handleResponse);
}

function getROC(id, project_id) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/models/${id}/blue-print/?project=${project_id}`, requestOptions).then(handleResponse);
}

function getBluePrint(id, project_id) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/models/${id}/roc/?project=${project_id}`, requestOptions).then(handleResponse);
}

function getFeatureImportance(id, project_id) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/models/${id}/feature-importance/?project=${project_id}`, requestOptions).then(handleResponse);
}

function getLossInteraction(id, project_id) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/models/${id}/loss-interaction/?project=${project_id}`, requestOptions).then(handleResponse);
}

function getActualPrediction(id, project_id) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/models/${id}/actual-prediction/?project=${project_id}`, requestOptions).then(handleResponse);
}


function getTrainingMetric() {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/training/metric/`, requestOptions).then(handleResponse);
}

function getMeta(id) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/meta/${id}/by-dataset/`, requestOptions).then(handleResponse);
}

function interruptTraining(id) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/training/${id}/interrupt/`, requestOptions).then(handleResponse);
}

function addProject(project) {
    let header = { 'Content-Type': 'application/json' }
    const requestOptions = {
        method: 'POST',
        headers: {...header, ...authHeader()},
        body: JSON.stringify(project)
    };
    return fetch(`${config.apiUrl}/apis/project/`, requestOptions).then(handleResponse);
}

function createTraining(detail) {
    let header = { 'Content-Type': 'application/json' }
    const requestOptions = {
        method: 'POST',
        headers: {...header, ...authHeader()},
        body: JSON.stringify(detail)
    };
    return fetch(`${config.apiUrl}/apis/training/`, requestOptions).then(handleResponse);
}

function addDataset(request, callback) {
    const requestOptions = {
        method: 'POST',
        headers: authHeader(),
        body: request
    };
    return fetch(`${config.apiUrl}/apis/dataset/upload/`, requestOptions).then(handleResponse);
}

function addTesting(request) {
    const requestOptions = {
        method: 'POST',
        headers: authHeader(),
        body: request
    };
    return fetch(`${config.apiUrl}/apis/testing/upload/`, requestOptions).then(handleResponse);
}

function deployModel(request) {
    let header = { 'Content-Type': 'application/json' }
    const requestOptions = {
        method: 'POST',
        headers: {...header, ...authHeader()},
        body: request
    };
    return fetch(`${config.apiUrl}/apis/deploy/`, requestOptions).then(handleResponse);
}

function getDeployedModel(id) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/deploy/${id}/by-project/`, requestOptions).then(handleResponse);
}

function getTestingGraph(id) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/deploy/${id}/graph/`, requestOptions).then(handleResponse);
}

function startTesting(id, project) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/deploy/${id}/testing/?project=${project}`, requestOptions).then(handleResponse);
}

function getTestingData(id) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/testing/${id}/by-dataset/`, requestOptions).then(handleResponse);
}

function getTaskProgress(id) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/project/${id}/task/`, requestOptions).then(handleResponse);
}

function deleteProject(id) {
    let header = { 'Content-Type': 'application/json' }
    const requestOptions = {
        method: 'DELETE',
        headers: {...header, ...authHeader()},
    };
    return fetch(`${config.apiUrl}/apis/project/${id}/`, requestOptions).then(handleResponse);
}

function deleteDataset(id) {
    let header = { 'Content-Type': 'application/json' }
    const requestOptions = {
        method: 'DELETE',
        headers: {...header, ...authHeader()},
    };
    return fetch(`${config.apiUrl}/apis/dataset/${id}/`, requestOptions).then(handleResponse);
}

function getProject(id) {
    let header = { 'Content-Type': 'application/json' }
    const requestOptions = {
        method: 'GET',
        headers: {...header, ...authHeader()},
    };
    return fetch(`${config.apiUrl}/apis/project/${id}/`, requestOptions).then(handleResponse);
}

function getType() {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };

    return fetch(`${config.apiUrl}/apis/meta/type/`, requestOptions).then(handleResponse);
}

function getRole() {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };

    return fetch(`${config.apiUrl}/apis/meta/role/`, requestOptions).then(handleResponse);
}

function getProblemType() {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/training/problem/`, requestOptions).then(handleResponse);
}

function getTimeType() {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/training/time/`, requestOptions).then(handleResponse);
}

function getImputation() {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };

    return fetch(`${config.apiUrl}/apis/meta/imputation/`, requestOptions).then(handleResponse);
}

function updateMeta(id, request) {
    const requestOptions = {
        method: 'PATCH',
        headers: authHeader(),
        body: request
    };
    return fetch(`${config.apiUrl}/apis/meta/${id}/`, requestOptions).then(handleResponse);
}

function getMetaConnections(id) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/connection/${id}/by-project/`, requestOptions).then(handleResponse);
}

function mergeConnections(id, request) {
    let header = { 'Content-Type': 'application/json' };
    const requestOptions = {
        method: 'POST',
        headers: {...header, ...authHeader()},
        body: request
    };
    return fetch(`${config.apiUrl}/apis/connection/${id}/merge/`, requestOptions).then(handleResponse);
}


function updateLoc(nodes) {
    let header = { 'Content-Type': 'application/json' };
    const requestOptions = {
        method: 'POST',
        headers: {...header, ...authHeader()},
        body: JSON.stringify(nodes)
    };
    return fetch(`${config.apiUrl}/apis/dataset/update-loc/`, requestOptions).then(handleResponse);
}


function getDatasetData(id, offset) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/apis/dataset/${id}/data/?offset=${offset}`, requestOptions).then(handleResponse);
}

function deleteConnection(id) {
    let header = { 'Content-Type': 'application/json' }
    const requestOptions = {
        method: 'DELETE',
        headers: {...header, ...authHeader()},
    };
    return fetch(`${config.apiUrl}/apis/connection/${id}/`, requestOptions).then(handleResponse);
}


function addConnection(request) {
    let header = { 'Content-Type': 'application/json' }
    const requestOptions = {
        method: 'POST',
        headers: {...header, ...authHeader()},
        body: request
    };
    return fetch(`${config.apiUrl}/apis/connection/`, requestOptions).then(handleResponse);
}