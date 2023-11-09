import { createEffect, createSignal, onMount, For } from "solid-js"

let [app, setApp] = createSignal("cherrypy")

function AddItem(props) {
  let element = (
    <form>
      <input name="name" placeholder="name" />
      <input name="description" placeholder="description" />
      <input type="submit" value="Submit"/>
    </form>
  )

  element.addEventListener("submit", function(event) {
    event.preventDefault()
    let body = new FormData(this)
    fetch(`https://api.spokanepython.com/${app()}/items`, {
      method: "POST",
      body: body
    }).then((resp) => {
      if (resp.status == 201) {
        props.update()
      }
      else {
        throw new Error("api failed to return 201")
      }
    }).catch((err) => console.error(err))
  })

  return element
}

function ClearItems(props) {
  let button
  let element = (
    <div ref={button}>
      <h5>Clear Items</h5>
    </div>
  )

  button.addEventListener("click", (event) => {
    fetch(`https://api.spokanepython.com/${app()}/items/`, {
      method: "DELETE",
    }).then((resp) => {
      if (resp.status == 204) {
        props.update()
      }
    })
  })

  return element
}

function Item(props) {
  let [name, setName] = createSignal("")
  let [description, setDescription] = createSignal("")
  let [timestamp, setTimestamp] = createSignal("")
  let [done, setDone] = createSignal("false")

  let url = props.url
  let update = props.update

  function sync(key, getter) {
    return function() {
      let body = new FormData()
      body.append(key, getter())
      console.log(body)
      fetch(url, {
        method: "PATCH",
        body: body,
      }).then((resp) => {
        console.log(resp)
        if (resp.status == 204) {
          update()
        }
      }).catch((err) => console.error(err))
    }
  }

  function Field(props) {
    let hook = props.hook
    let name = props.name
    let element = (
      <input type="text" value={hook()}/>
    )
    let getter = () => element.value
    element.addEventListener("change", sync(name, getter))
    return element
  }

  function Check(props) {
    let name = props.name
    let element = (
      <input type="checkbox" checked={() => done()}/>
    )
    let getter = () => element.checked
    createEffect(() => {
      element.checked = done() === "true"
    })
    element.addEventListener("change", sync(name, getter))
    return element
  }

  let element = (
    <div>
      <Field name="name" hook={name}/>
      <Field name="description" hook={description}/>
      <Field name="timestamp" hook={timestamp}/>
      <Check name="done"/>
    </div>
  )

  function getData() {
    fetch(props.url
    ).then((resp) => resp.json()
    ).then((resp) => resp.item
    ).then((resp) => {
      let key = Object.keys(resp).pop()
      return resp[key]
    }).then((resp) => {
      console.log(resp)
      setName(resp.name)
      setDescription(resp.description)
      setTimestamp(resp.timestamp)
      setDone(resp.done)
    })
  }

  onMount(getData)
  return element
}

export function Items(props) {
  let [items, setItems] = createSignal({})
  function update() {
    fetch(
      `https://api.spokanepython.com/${app()}/items/`
    ).then((resp) => {
      return resp.json()
    }).then((resp) => {
      setItems(() => resp.items)
    })
  }
  onMount(update)

  function AppSelector() {
    let element = (
      <select>
        <option value="cherrypy">CherryPy</option>
        <option value="flask">Flask</option>
        <option value="fastapi">FastAPI</option>
      </select>
    )
    element.addEventListener("change", (event) => {
      setApp(element.value)
      console.log(app())
    })
    return element
  }
  let element = (
    <>
      <div>
        <h1>items</h1>
        <AppSelector />
      </div>
      <div>
        <h5>Add Item</h5>
      </div>
      <AddItem update={update}/>
      <br />
      <For each={items()}>
        {(item, idx) => {
          return <Item update={update} url={item}/>
        }}
      </For>
      <ClearItems update={update}/>
    </>
  )

  return element
}
