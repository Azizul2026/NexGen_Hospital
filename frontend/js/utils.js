const API_BASE = 'http://127.0.0.1:8000/api';

function getToken(){
  return localStorage.getItem('nexgen_token');
}

async function apiRequest(path, method='GET', body=null){
  try{
    const res = await fetch(API_BASE + path, {
      method,
      headers:{
        'Content-Type':'application/json',
        ...(getToken() && {Authorization:`Bearer ${getToken()}`})
      },
      ...(body && {body: JSON.stringify(body)})
    });

    const json = await res.json().catch(()=>({}));

    if(!res.ok){
      if(res.status === 401){
        logout();
      }
      throw new Error(json.message || 'API Error');
    }

    return json;

  }catch(err){
    toast(err.message,'error');
    return {success:false};
  }
}