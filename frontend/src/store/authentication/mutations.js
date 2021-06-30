export function auth_success(state, token, user) {
  state.status = 'success'
}

export function auth_error(state){
  state.status = 'error'
}

export function logout(state){
  state.status = ''
}
