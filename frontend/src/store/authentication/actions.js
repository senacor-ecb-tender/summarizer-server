/*
export function someAction (context) {
}
*/

export function login({commit}, username, password) {
  return new Promise((resolve, reject) => {
    this.$axios({
      url: 'login', method: 'GET',
      auth: {
        username: username,
        password: password
      }
    })
      .then(resp => {
        commit('auth_success')
        resolve(resp)
      })
      .catch(err => {
        commit('auth_error')
        reject(err)
      })
  })
}

export function logout({commit}) {
  return new Promise((resolve, reject) => {
    commit('logout')
    resolve()
  })
}
