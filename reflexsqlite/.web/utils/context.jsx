import React, { useContext, useMemo, useState, createElement, useEffect } from "react"
import { applyDelta, ReflexEvent, hydrateClientStorage, useEventLoop, refs } from "$/utils/state"
import { ColorModeContext, UploadFilesContext, DispatchContext, EventLoopContext, StateStoreContext, registerApp, eventLoop } from "$/utils/context-registry"
import { jsx } from "@emotion/react";

// Disable React dev-build owner-stack capture: the per-element Error()
// dominates dev-mode render CPU on large pages. Costs owner frames in
// `React.captureOwnerStack()`; set REFLEX_REACT_OWNER_STACKS=1 to restore.
// Full context: https://github.com/reflex-dev/reflex/pull/6905
if (typeof window !== "undefined") {
  try {
    const reactInternals =
      React.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE;
    const ownerStackCounterKey = "recentlyCreatedOwnerStacks";
    if (
      reactInternals &&
      typeof reactInternals[ownerStackCounterKey] === "number"
    ) {
      Object.defineProperty(reactInternals, ownerStackCounterKey, {
        get: () => 1e9,
        set: () => {},
        configurable: true,
      });
    }
  } catch {}
}

export { ColorModeContext, UploadFilesContext, DispatchContext, EventLoopContext, StateStoreContext };
export const initialState = {"reflex___state____state": {"is_hydrated_rx_state_": false, "rx_router_headers_rx_state_": {"host": "", "origin": "", "upgrade": "", "connection": "", "pragma": "", "cache_control": "", "user_agent": "", "sec_websocket_version": "", "sec_websocket_key": "", "sec_websocket_extensions": "", "accept_encoding": "", "accept_language": "", "raw_headers": {}}, "rx_router_page_rx_state_": {"host": "", "path": "", "raw_path": "", "full_path": "", "full_raw_path": "", "params": {}}, "rx_router_route_id_rx_state_": "", "rx_router_session_rx_state_": {"client_token": "", "client_ip": "", "session_id": ""}, "rx_router_url_rx_state_": {"scheme": "", "netloc": "", "origin": "://", "path": "", "query": "", "query_parameters": {}, "fragment": "", "href": ""}}, "reflex___state____state.reflex___istate___shared____shared_state_base_internal": {}, "reflex___state____state.reflex___state____frontend_event_exception_state": {}, "reflex___state____state.reflex___state____on_load_internal_state": {}, "reflex___state____state.reflex___state____update_vars_internal_state": {}, "reflex___state____state.reflexsqlite___state___base____auth_state": {"auth_busy_rx_state_": false, "auth_error_rx_state_": "", "auth_notice_rx_state_": "", "avatar_color_rx_state_": "#4F46E5", "display_name_rx_state_": "Guest", "email_rx_state_": "", "full_name_rx_state_": "", "initials_rx_state_": "?", "is_authenticated_rx_state_": false, "login_name_rx_state_": "", "login_password_rx_state_": "", "reg_confirm_rx_state_": "", "reg_email_rx_state_": "", "reg_full_name_rx_state_": "", "reg_password_rx_state_": "", "reg_username_rx_state_": "", "role_rx_state_": "", "token_rx_state_": "", "user_id_rx_state_": 0, "username_rx_state_": ""}, "reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state": {"active_dataset_id_rx_state_": 0, "active_name_rx_state_": "", "activity_rx_state_": [], "categorical_rx_state_": [], "chart_data_rx_state_": [], "chart_subtitle_rx_state_": "Primary metric for ", "chart_type_rx_state_": "line", "columns_rx_state_": [], "corr_grid_columns_rx_state_": "repeat(1, minmax(0, 1fr))", "corr_labels_rx_state_": [], "corr_rows_rx_state_": [], "dashboard_error_rx_state_": "", "datasets_rx_state_": [], "has_datasets_rx_state_": false, "kpi_columns_rx_state_": "0", "kpi_completeness_rx_state_": "0%", "kpi_datasets_rx_state_": "0", "kpi_missing_rx_state_": "0", "kpi_rows_rx_state_": "0", "live_data_rx_state_": [], "live_enabled_rx_state_": true, "live_running_rx_state_": false, "missing_hint_rx_state_": "0 missing cells", "numeric_rx_state_": [], "refresh_seconds_rx_state_": 3, "stats_rx_state_": {}, "tick_rx_state_": 0, "x_column_rx_state_": "", "x_options_rx_state_": [], "y_column_rx_state_": "", "y_options_rx_state_": []}, "reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state": {"active_dataset_id_rx_state_": 0, "active_name_rx_state_": "No dataset selected", "categorical_rx_state_": [], "columns_rx_state_": [], "dataset_search_rx_state_": "", "datasets_rx_state_": [], "detail_rx_state_": {}, "editing_row_id_rx_state_": 0, "error_rx_state_": "", "form_values_rx_state_": {}, "has_datasets_rx_state_": false, "is_uploading_rx_state_": false, "meta_description_rx_state_": "", "meta_name_rx_state_": "", "notice_rx_state_": "", "numeric_rx_state_": [], "page_rx_state_": 1, "page_count_rx_state_": 1, "page_size_rx_state_": 10, "row_search_rx_state_": "", "show_add_dialog_rx_state_": false, "show_edit_dialog_rx_state_": false, "show_meta_dialog_rx_state_": false, "table_rows_rx_state_": [], "total_rows_rx_state_": 0, "upload_description_rx_state_": "", "upload_error_rx_state_": "", "upload_message_rx_state_": ""}, "reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state": {"active_dataset_id_rx_state_": 0, "active_library_rx_state_": "pandas", "active_library_color_rx_state_": "#7069D1", "active_library_name_rx_state_": "Pandas", "active_op_description_rx_state_": "", "active_operation_rx_state_": "describe", "categorical_rx_state_": [], "columns_rx_state_": [], "datasets_rx_state_": [], "explore_error_rx_state_": "", "has_result_rx_state_": false, "has_result_chart_rx_state_": false, "is_running_rx_state_": false, "library_available_rx_state_": true, "library_version_rx_state_": "2.3.3", "needs_x_rx_state_": false, "needs_y_rx_state_": false, "numeric_rx_state_": [], "operations_rx_state_": [], "result_chart_rx_state_": [], "result_chart_label_rx_state_": "Value", "result_color_rx_state_": "#4F46E5", "result_elapsed_rx_state_": 0, "result_elapsed_label_rx_state_": "", "result_image_rx_state_": "", "result_library_rx_state_": "", "result_metrics_rx_state_": [], "result_notes_rx_state_": [], "result_secondary_rx_state_": false, "result_secondary_label_rx_state_": "", "result_summary_rx_state_": "", "result_table_columns_rx_state_": [], "result_table_rows_rx_state_": [], "result_title_rx_state_": "", "x_column_rx_state_": "", "x_options_rx_state_": [], "y_column_rx_state_": "", "y_options_rx_state_": []}, "reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___settings_state____settings_state": {"avatar_color_rx_state_": "#4F46E5", "chart_type_rx_state_": "line", "confirm_password_rx_state_": "", "current_password_rx_state_": "", "default_library_rx_state_": "pandas", "live_enabled_rx_state_": true, "live_refresh_seconds_rx_state_": "3", "new_password_rx_state_": "", "profile_email_rx_state_": "", "profile_name_rx_state_": "", "profile_role_rx_state_": "", "profile_username_rx_state_": "", "rows_per_page_rx_state_": "10", "settings_error_rx_state_": "", "settings_ok_rx_state_": "", "show_advanced_rx_state_": false, "theme_rx_state_": "light"}}
export const initialStateHashes = ["02933a31ca51d977", "d029e8db883816fc", "bf21a9e8fbc5a384", "bf21a9e8fbc5a384", "bf21a9e8fbc5a384", "bf21a9e8fbc5a384", "a08317240d376f08", "300febe7f451379f", "f4e496685d2b338d", "4324177c02b53b26", "ff0156ad7842a174"]
export const stateSchema = "3acce8d6d30c7ed9e553fdd31e801ce8"

export const defaultColorMode = "system"
export const clientStorage = {"cookies": {"reflex___state____state.reflexsqlite___state___base____auth_state.token_rx_state_": {"name": "df_session", "path": "/", "maxAge": 604800, "sameSite": "lax"}}, "local_storage": {}, "session_storage": {}}


export const state_name = "reflex___state____state"

export const exception_state_name = "reflex___state____state.reflex___state____frontend_event_exception_state"

// Tracked cookie and local storage vars set in the browser, or undefined if none.
const clientStorageVars = () => {
    const client_storage_vars = hydrateClientStorage(clientStorage);
    if (client_storage_vars && Object.keys(client_storage_vars).length !== 0) {
        return client_storage_vars;
    }
    return undefined;
}

// These events are triggered on each client-side page navigation.
export const onLoadInternalEvent = () => {
    const internal_events = [];

    // Only send the client storage vars if any are actually set in the browser.
    const client_storage_vars = clientStorageVars();
    if (client_storage_vars !== undefined) {
        internal_events.push(
            ReflexEvent(
                'reflex___state____state.reflex___state____update_vars_internal_state.update_vars_internal',
                {vars: client_storage_vars},
            ),
        );
    }

    // `on_load_internal` triggers the correct on_load event(s) for the current page.
    // If the page does not define any on_load event, this will just set `is_hydrated = true`.
    internal_events.push(ReflexEvent('reflex___state____state.reflex___state____on_load_internal_state.on_load_internal'));

    return internal_events;
}

// The single event sent when the websocket connects or reconnects: it resets and
// applies client storage, sends the state, and queues the page's on_load events.
// On the first connect the frontend still holds the compiled defaults, so it
// sends their hashes and the backend only returns the vars that differ; any
// later (re)hydrate gets the full state.
export const initialEvents = (first = false) => {
    const client_storage_vars = clientStorageVars();
    const payload = {};
    if (client_storage_vars !== undefined) {
        payload["vars"] = client_storage_vars;
    }
    if (first) {
        payload["hashes"] = initialStateHashes;
    }
    return [ReflexEvent('reflex___state____state.hydrate_and_load', payload)];
}
    

export const isDevMode = true;

// The static runtime reads these through the registry, so this module is the
// only one Vite re-executes when they change.
registerApp({
  initialState,
  clientStorage,
  state_name,
  stateSchema,
  exception_state_name,
  onLoadInternalEvent,
  initialEvents,
  isDevMode,
  defaultColorMode,
});

export function addEvents(events, args, event_actions) {
  return eventLoop.addEvents(events, args, event_actions);
}

export function getConnectErrors() {
  return eventLoop.connectErrors;
}

export function UploadFilesProvider({ children }) {
  const [filesById, setFilesById] = useState({})
  refs["__clear_selected_files"] = (id) => setFilesById(filesById => {
    const newFilesById = {...filesById}
    delete newFilesById[id]
    return newFilesById
  })
  return createElement(
    UploadFilesContext.Provider,
    { value: [filesById, setFilesById] },
    children
  );
}

// ``displayName`` is what React DevTools shows for the wrapper; without it
// every client-only component in the tree renders as ``Anonymous``.
export function ClientSide(component, name) {
  function ClientSideComponent({ children, ...props }) {
    const [Component, setComponent] = useState(null);
    useEffect(() => {
      async function load() {
        const comp = await component();
        setComponent(() => comp);
      }
      load();
    }, []);
    return Component ? jsx(Component, props, children) : null;
  }
  ClientSideComponent.displayName = name ? `ClientSide(${name})` : "ClientSide";
  return ClientSideComponent;
}

export function EventLoopProvider({ children }) {
  const dispatch = useContext(DispatchContext)
  const [addEventsLocal, connectErrors] = useEventLoop(
    dispatch,
    initialEvents,
    clientStorage,
  )
  // Publish the dispatchers so JSX literals constructed outside the
  // React-tree path (e.g. ``ErrorBoundary.onError``) can call ``addEvents``.
  eventLoop.addEvents = addEventsLocal;
  eventLoop.connectErrors = connectErrors;
  return useMemo(
    () =>
      createElement(
        EventLoopContext.Provider,
        { value: [addEventsLocal, connectErrors] },
        children
      ),
    [addEventsLocal, connectErrors, children],
  );
}

// Dispatch updates happen outside render; useSyncExternalStore keeps reads
// consistent while notifying only consumers of the changed substate.
function createStateStore(initialState) {
  const state = {};
  const listeners = new Map();
  const dispatchers = {};
  const notify = (substateName) =>
    listeners.get(substateName)?.forEach((listener) => listener());
  // Hot reload passes the recompiled initial state: new substates are added,
  // and existing substates gain new fields at their defaults while keeping
  // their live values.
  const mergeInitialState = (nextInitialState) => {
    for (const [substateName, value] of Object.entries(nextInitialState)) {
      const liveState = state[substateName];
      if (liveState !== undefined) {
        if (Object.keys(value).some((key) => !Object.hasOwn(liveState, key))) {
          state[substateName] = { ...value, ...liveState };
          notify(substateName);
        }
        continue;
      }
      state[substateName] = value;
      dispatchers[substateName] = (delta) => {
        const currentState = state[substateName];
        const nextState = applyDelta(currentState, delta);
        if (nextState === currentState) return;
        state[substateName] = nextState;
        notify(substateName);
      };
      notify(substateName);
    }
  };
  mergeInitialState(initialState);

  return {
    dispatchers,
    mergeInitialState,
    getSnapshot: (substateName) => state[substateName],
    subscribe: (substateName, listener) => {
      let substateListeners = listeners.get(substateName);
      if (!substateListeners) {
        substateListeners = new Set();
        listeners.set(substateName, substateListeners);
      }
      substateListeners.add(listener);
      return () => substateListeners.delete(listener);
    },
  };
}

function StateStoreProviders({ children, store }) {
  return createElement(
    StateStoreContext,
    { value: store },
    createElement(DispatchContext, { value: store.dispatchers }, children),
  );
}

function ClientStateProvider({ children }) {
  const [store] = useState(() => createStateStore(initialState));
  useEffect(() => store.mergeInitialState(initialState), [store, initialState]);
  return createElement(StateStoreProviders, { children, store });
}

// The server renders once and never applies a delta, so it only reads the
// initial state.
const serverStateStore = {
  dispatchers: {},
  getSnapshot: (substateName) => initialState[substateName],
  subscribe: () => () => {},
};

function ServerStateProvider({ children }) {
  return createElement(StateStoreProviders, { children, store: serverStateStore });
}

export const StateProvider =
  typeof document === "undefined" ? ServerStateProvider : ClientStateProvider;