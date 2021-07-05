<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <!-- Header toolbar -->
      <q-toolbar>
        <q-btn
          aria-label="Menu"
          dense
          flat
          icon="menu"
          round
          @click="leftDrawerOpen = !leftDrawerOpen"
        />

        <q-toolbar-title class="ecb-font-bold">
          Text Summarizer
        </q-toolbar-title>
        <q-space/>
        <div class="q-gutter-sm row items-center no-wrap ecb-font-regular">
          <q-btn v-if="!isLoggedIn" color="white" icon="login" label="Login" push size="sm"
                 text-color="primary" @click="showLogin = true">
            <q-tooltip>Login</q-tooltip>
          </q-btn>
          <q-btn v-if="isLoggedIn" color="white" icon="menu_book" label="Summarize" push size="sm"
                 text-color="primary" @click="showSummaryDialog = true">
            <q-tooltip>Run summarization</q-tooltip>
          </q-btn>
          <q-btn v-if="isLoggedIn" color="white" icon="logout" label="Logout" push size="sm"
                 text-color="primary" @click="logout">
            <q-tooltip>Logout</q-tooltip>
          </q-btn>
          <q-space/>

        </div>
      </q-toolbar>
    </q-header>

    <!-- Left side menu -->
    <q-drawer
      v-model="leftDrawerOpen"
      bordered
      content-class="bg-white"
    >
      <q-list>
        <q-item-label
          class="text-primary text-bold ecb-font-regular"
          header
        >
          Our Application
        </q-item-label>

        <EssentialLink
          v-for="link in linksDataMain"
          :key="link.title"
          v-bind="link"
        />
        <q-item-label
          class="text-primary text-bold ecb-font-regular"
          header
        >
          Used Frameworks
        </q-item-label>
        <EssentialLink
          v-for="link in linksDataFrameworks"
          :key="link.title"
          v-bind="link"
        />
        <q-item-label
          class="text-primary text-bold ecb-font-regular"
          header
        >
          Infrastructure
        </q-item-label>
        <EssentialLink
          v-for="link in linksDataInfrastructure"
          :key="link.title"
          v-bind="link"
        />
      </q-list>

    </q-drawer>

    <!-- Login dialog -->
    <q-dialog ref="login" v-model="showLogin">
      <div class="row">
        <q-card square bordered class="q-pa-lg shadow-1">
          <q-card-section>
            <q-form class="q-gutter-md">
              <q-input square filled clearable v-model="username" type="username" label="Username"/>
              <q-input square filled clearable v-model="password" type="password" label="Password"/>
            </q-form>
          </q-card-section>
          <q-card-actions class="q-px-md">
            <q-btn unelevated color="primary" size="sm" class="full-width" label="Login" @click="login"/>
          </q-card-actions>
        </q-card>
      </div>
    </q-dialog>

    <!-- Summary run dialog -->
    <q-dialog v-model="showSummaryDialog" full-height full-width @close="reset" @hide="reset">
      <div class="row" style="overflow: auto; height: inherit;">
        <div class="col-3" style="background-color: white;">
          <q-card flat square style="overflow: auto;">
            <q-card-section>
              <div class="text-h6 text-primary">Setup</div>
            </q-card-section>
            <q-card-actions align="center">
              <q-btn :disabled="!isComplete" color="primary" label="Summarize" size="sm" unelevated
                     @click="$refs.uploader.upload()">
                <q-tooltip>Run summarization</q-tooltip>
              </q-btn>
              <q-btn color="primary" label="Reset" size="sm" unelevated @click="reset()">
                <q-tooltip>Reset</q-tooltip>
              </q-btn>
              <q-btn color="primary" label="Close" size="sm" unelevated @click="close()">
                <q-tooltip>Close</q-tooltip>
              </q-btn>
            </q-card-actions>
            <q-card-section>
              <q-banner dense>
                <template v-slot:avatar>
                  <q-icon name="info" color="info" />
                </template>
              Creating the summarization will typically take 10-20 minutes and can take up to 60 minutes.
              </q-banner>
            </q-card-section>
            <q-card-section>
              <q-select
                v-model="topicType"
                :options="optionsTopic"
                dense
                label="Select Topic"
                option-label="label"
                option-value="id"
                outlined
                style="overflow: auto;">
                <template v-slot:prepend>
                  <q-icon name="my_location"/>
                </template>
              </q-select>
            </q-card-section>
            <q-card-section>
              <q-select
                v-model="summaryType"
                :options="optionsSummary"
                dense
                label="Select Size Of Summary"
                option-label="label"
                option-value="id"
                outlined
                style="overflow: auto;">
                <template v-slot:prepend>
                  <q-icon name="article"/>
                </template>
              </q-select>
            </q-card-section>
            <q-card-section>
              <q-uploader
                ref="uploader"
                :factory="factoryFn"
                accept=".txt"
                bordered
                color="white"
                flat
                hide-upload-btn
                label="Textfile"
                style="overflow: auto; width: inherit"
                text-color="black"
                @added="setFileSelected"
                @failed="failed"
                @removed="unsetFileSelected"
                @uploaded="summarize"
              />
            </q-card-section>

          </q-card>
        </div>
        <q-separator v-if="summaryVisible" color="primary" vertical/>
        <div v-if="summaryVisible" class="col-6" style="background-color: white; overflow-wrap: break-word;">

          <q-card flat square style="overflow: auto;">
            <q-card-section>
              <div class="text-h6 text-primary">Summary</div>
            </q-card-section>

            <q-card-actions align="center">
              <q-btn color="primary" label="Download" size="sm" unelevated
                     @click="exportSummary">
                <q-tooltip>Export summary to Textfile</q-tooltip>
              </q-btn>
            </q-card-actions>
            <q-card-section>
              <span v-html="summarization"></span>
            </q-card-section>
          </q-card>
        </div>
        <div v-if="summaryVisible" class="col-2" style="background-color: aliceblue;">
          <q-card flat square style="overflow: auto; background-color: aliceblue;">
            <q-card-section>
              <div class="text-h6 text-primary">Rating</div>
            </q-card-section>
            <q-card-actions align="center">
              <q-btn color="primary" disabled label="Rate" size="sm" unelevated>
                <q-tooltip>Save rating</q-tooltip>
              </q-btn>
            </q-card-actions>

            <q-card-section>
              <q-rating
                v-model="ratingModel"
                color="primary"
                icon="star_border"
                icon-selected="star"
                size="1.5em"
              />
            </q-card-section>
            <q-card-section>
              By rating the quality of the summary you can improve
              the model quality by providing better training data
              for future model tuning.
              <br><br>
              This feature is not implemented yet.
            </q-card-section>

          </q-card>
        </div>
      </div>
    </q-dialog>

    <q-page-container>
      <router-view/>
    </q-page-container>
  </q-layout>


</template>

<script>

import EssentialLink from 'components/EssentialLink.vue'
import {ref} from 'vue'
import {exportFile, useQuasar} from 'quasar'

/**
 * Link definitions for side menu
 */

const linksDataMain = [
  {
    title: 'Our Code',
    caption: 'See code repository',
    icon: 'code',
    link: 'https://github.com/senacor-ecb-tender/summarizer-server'
  }
];

const linksDataFrameworks = [
  {
    title: 'FastAPI',
    caption: 'Lightweight python web framework',
    icon: 'local_library',
    link: 'https://fastapi.tiangolo.com/'
  },
  {
    title: 'Hugging Face',
    caption: 'State of the art Natural Language Processing',
    icon: 'local_library',
    link: 'https://huggingface.co/'
  },
  {
    title: 'Quasar',
    caption: 'Vue.js based frontend framework',
    icon: 'local_library',
    link: 'https://quasar.dev/'
  }
];
const linksDataInfrastructure = [
  {
    title: 'Azure Machine Learning',
    caption: 'Managed machine learning services',
    icon: 'Isettings_input_composite',
    link: 'https://docs.microsoft.com/de-de/azure/machine-learning/overview-what-is-azure-ml'
  },
  {
    title: 'Azure Kubernetes Service',
    caption: 'Fully managed Kubernetes',
    icon: 'settings_input_composite',
    link: 'https://azure.microsoft.com/en-us/services/kubernetes-service//'
  },
  {
    title: 'Azure Static Web Apps',
    caption: 'Serverless web app hosting',
    icon: 'settings_input_composite',
    link: 'https://azure.microsoft.com/en-us/services/app-service/static'
  },
  {
    title: 'GitHub',
    caption: 'Git repository hosting',
    icon: 'settings_input_composite',
    link: 'https://github.com/'
  }
];

// main component code
export default {
  name: 'MainLayout',
  components: {EssentialLink},
  data() {
    return {
      leftDrawerOpen: false,
      linksDataMain: linksDataMain,
      linksDataFrameworks: linksDataFrameworks,
      linksDataInfrastructure: linksDataInfrastructure,
      optionsTopic: [
        {
          id: 'asset_quality',
          label: 'Asset Quality'
        },
        {
          id: 'climate_risk',
          label: 'Climate Risk'
        },
        {
          id: 'pandemic',
          label: 'Pandemic'
        },
        {
          id: 'credit_lending',
          label: 'Credit Lending'
        }
      ],
      optionsSummary: [
        {
          id: 'long',
          label: 'Long version (9-15 sentences)'
        },
        {
          id: 'short',
          label: 'Short version (3-6 sentences)'
        }
      ],
      // fields for summary dialog
      showSummaryDialog: false,
      topicType: "",
      summaryType: "",
      fileSelected: false,
      summarization: "...",
      summaryVisible: false,

      // fields for login dialoh
      showLogin: false,
      username: '',
      password: ''
    }
  },

  // code for error message when backend-error occurs
  setup() {
    const $q = useQuasar()
    return {
      ratingModel: ref(0),
      failed(info) {
        $q.notify({
          type: 'negative',
          message: 'Call to Summarization API failed!'
        })
      }
    }
  },

  // comouted properties to see whether user ist logged in or summary run finished
  computed: {
    isComplete() {
      return this.topicType != "" && this.summaryType != "" && this.fileSelected;
    },
    isLoggedIn() {
      console.log(this.$store.getters["authentication/isLoggedIn"])
      return this.$store.getters["authentication/isLoggedIn"]
    }
  },
  methods: {
    // export summary as .txt-file
    exportSummary() {
      const $q = useQuasar()

      const status = exportFile('summary.txt', this.summarization.replaceAll("<br/>", "\n"), {
        encoding: 'UTF-8',
        mimeType: 'text/plain;charset=UTF-8;'
      })

      if (status === true) {
        // browser allowed it
      } else {
        // browser denied it
        $q.notify({
          type: 'negative',
          message: 'Browser does not allow the export: Error code ' + status
        })
      }
    },

    // file upploader status changes
    setFileSelected() {
      this.fileSelected = true
    },
    unsetFileSelected() {
      this.fileSelected = false
    },

    // reset summary dialog
    reset() {
      this.summaryVisible = false
      this.summaryType = ""
      this.topicType = ""
      this.fileSelected = false
      this.$refs.uploader.reset()
    },

    // close summary dialog
    close() {
      this.showSummaryDialog = false
    },

    // call of upload-endpoint to start summary process on backend
    factoryFn(files) {
      return {
        url: process.env.API + '/upload',
        method: 'POST',
        fieldName: 'file',
        formFields: [{name: 'topic', value: this.topicType.id}, {name: 'summary_type', value: this.summaryType.id}]
      }
    },

    // pre-process summary result for GUI
    summarize({files, xhr}) {
      let result;
      let text;
      let lineNum = 1;
      result = JSON.parse(xhr.response).result
      text = ""
      result.forEach(line => {
        text = text + lineNum + '. ' + line + '<br/><br/>'
        lineNum = lineNum + 1
      })

      this.summarization = text
      this.summaryVisible = true
    },

    // login/logout logic
    login() {
      this.$refs.login.hide()
      this.$store.dispatch("authentication/login", {username: this.username, password: this.password})
    },
    logout() {
      this.$store.dispatch("authentication/logout")
    }
  }
}
</script>
