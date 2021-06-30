/*
export function someGetter (state) {
}
*/

export function isLoggedIn(state) {
  if (state.status == 'success') {
    return true
  }
  else {
    return false
  }
}
