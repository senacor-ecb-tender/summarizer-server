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
        commit('auth_error')
      })
  })
}

export function logout({commit}) {
  return new Promise((resolve, reject) => {
    commit('logout')
  })
}
