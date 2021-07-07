/*
export function someAction (context) {
}
*/
import { document_api } from 'boot/axios'

export function login({commit}, payload) {
  return new Promise((resolve, reject) => {
    document_api.get('login', {
      auth: {
        username: payload.username,
        password: payload.password
      }
    })
      .then(resp => {
        commit('auth_success')
      })
      .catch(err => {
        if (err.response) {
          if (err.response.status == 401) {
            commit('auth_error')
          }
          else {
            commit('auth_error_other')
          }
        }

      })
  })
}

export function logout({commit}) {
  return new Promise((resolve, reject) => {
    commit('logout')
  })
}
