import { createEffect, createSignal, onMount, For } from "solid-js"

let [app, setApp] = createSignal("cherrypy")

function AddItem(props) {
  let element = (
    <form style={{ maxWidth: "300px", margin: "0 auto", padding: "20px", border: "1px solid #ccc", borderRadius: "5px", boxShadow: "0 2px 5px rgba(0, 0, 0, 0.1)" }}>
      <input style={{ width: "100%", padding: "8px", marginBottom: "16px", boxSizing: "border-box", borderRadius: "3px", border: "1px solid #ccc" }} name="name" placeholder="Name" />
      <textarea style={{ width: "100%", padding: "8px", marginBottom: "16px", boxSizing: "border-box", borderRadius: "3px", border: "1px solid #ccc" }} name="description" placeholder="Description"></textarea>
      <input style={{ backgroundColor: "#4CAF50", color: "white", padding: "10px 15px", border: "none", borderRadius: "3px", cursor: "pointer" }} type="submit" value="Submit" />
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
      fetch(url, {
        method: "PATCH",
        body: body,
      }).then((resp) => {
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
      <input
        type="text"
        value={hook()}
        style={{width: "100%", padding: "8px", marginBottom: "16px", boxSizing: "border-box", borderRadius: "3px", border: "1px solid #ccc"}}
      />
    )
    let getter = () => element.value
    element.addEventListener("change", sync(name, getter))
    return element
  }

  function Check(props) {
    let name = props.name
    let element = (
      <input
        type="checkbox"
        checked={() => done()}
        style={{ marginBottom: "16px" }}
      />
    )
    let getter = () => element.checked
    createEffect(() => {
      element.checked = done() === "true"
    })
    element.addEventListener("change", sync(name, getter))
    return element
  }

  let element = (
    <div style={{ padding: "20px", border: "1px solid #ddd", borderRadius: "10px", marginBottom: "20px" }}>
      <Field name="name" hook={name} />
      <Field name="description" hook={description} />
      <Field name="timestamp" hook={timestamp} />
      <Check name="done" />
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
    })
    return element
  }
  let element = (
    <>
      <AppSelector />
      <h5>Add Item</h5>
      <AddItem update={update}/>
      <br />
      <h5>Items</h5>
      <For each={items()}>
        {(item, _) => {
          return <Item update={update} url={item}/>
        }}
      </For>
      <ClearItems update={update}/>
    </>
  )

  return element
}
